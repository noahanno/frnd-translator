import os
import streamlit as st
from dotenv import load_dotenv
import requests
import re
import emoji

# Load environment variables
load_dotenv()
API_KEY = os.getenv("SARVAM_API_KEY", st.secrets.get("SARVAM_API_KEY", ""))

st.set_page_config(page_title="FRND Quality Translator", layout="wide")

# -------------------- CONFIG -------------------- #
LANG_MAP = {
    "Hindi": "hi-IN", "Kannada": "kn-IN", "Telugu": "te-IN", "Tamil": "ta-IN", "Malayalam": "ml-IN",
    "Bengali": "bn-IN", "Gujarati": "gu-IN", "Punjabi": "pa-IN", "Marathi": "mr-IN", "Odia": "or-IN",
    "English": "en-IN"
}

# Language-specific script and code-mixing preferences
LANGUAGE_PATTERNS = {
    "hi-IN": {
        "script": "roman",  # Heavy romanization
        "code_mixing": "heavy",  # Lots of English preserved
        "mode": "code-mixed",
        "style": "casual_roman"
    },
    "te-IN": {
        "script": "roman",  # Heavy romanization
        "code_mixing": "heavy",  # Lots of English preserved
        "mode": "code-mixed", 
        "style": "casual_roman"
    },
    "ta-IN": {
        "script": "mixed",  # Tamil script + English words
        "code_mixing": "moderate",  # Some English preserved
        "mode": "modern-colloquial",
        "style": "native_with_english"
    },
    "ml-IN": {
        "script": "fully-native",  # Mostly Malayalam script
        "code_mixing": "light",  # Most things translated
        "mode": "formal",
        "style": "native_script"
    },
    "kn-IN": {
        "script": "fully-native",  # Mostly Kannada script
        "code_mixing": "light",  # Most things translated
        "mode": "formal",
        "style": "native_script"
    }
}

# Enhanced mode options
MODE_OPTIONS = {
    "Modern & Casual (Default)": "modern-colloquial",
    "Formal / Professional": "formal", 
    "Word-for-Word / Literal": "classic-colloquial",
    "Blended (English + Indian)": "code-mixed"
}

# Context-aware settings
CONTEXT_TYPES = {
    "Marketing/Promotional": "Use engaging, persuasive language with appropriate code-mixing",
    "Technical Support": "Use clear, helpful, problem-solving tone",
    "Payment/Financial": "Use formal, trustworthy language", 
    "Festival/Cultural": "Use warm, celebratory, culturally appropriate tone",
    "Customer Service": "Use polite, empathetic, solution-oriented tone",
    "Urgent/Emergency": "Use direct, clear, action-oriented language"
}

AUDIENCE_TYPES = {
    "Young Adults (18-30)": "casual, trendy expressions with natural code-mixing",
    "Middle-aged (30-50)": "respectful, professional tone",
    "Senior Citizens (50+)": "formal, respectful, clear language", 
    "Business Professionals": "formal, professional terminology"
}

# Regional variations
REGIONAL_VARIANTS = {
    "hi-IN": ["Standard Hindi", "Delhi Hindi", "Mumbai Hindi", "UP Hindi"],
    "ta-IN": ["Standard Tamil", "Chennai Tamil", "Madurai Tamil", "Literary Tamil"],
    "te-IN": ["Standard Telugu", "Hyderabad Telugu", "Coastal Telugu", "Rayalaseema Telugu"], 
    "kn-IN": ["Standard Kannada", "Bangalore Kannada", "Mysore Kannada", "North Karnataka"],
    "ml-IN": ["Standard Malayalam", "Kochi Malayalam", "Thiruvananthapuram Malayalam"]
}

# Load preserved words
try:
    with open("preserve_words.txt", "r") as f:
        PRESERVE_WORDS = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    PRESERVE_WORDS = []

# -------------------- ENHANCED HELPER FUNCTIONS -------------------- #
def get_language_specific_settings(target_lang):
    """Get optimized settings for each language based on desired patterns"""
    if target_lang in LANGUAGE_PATTERNS:
        return LANGUAGE_PATTERNS[target_lang]
    else:
        # Default fallback
        return {
            "script": "roman",
            "code_mixing": "moderate", 
            "mode": "modern-colloquial",
            "style": "mixed"
        }

def enhance_preserve_words_for_language(target_lang):
    """Add language-specific words that should be preserved"""
    base_preserved = PRESERVE_WORDS.copy()
    
    # Common English words that should stay in English for heavy code-mixing languages
    if target_lang in ["hi-IN", "te-IN"]:
        english_tech_words = [
            "Hey", "Quick", "Update", "Status", "Online", "Offline", "Active", 
            "Audio", "Video", "Call", "Calls", "Chat", "Message", "Notification",
            "Platform", "Safe", "Earn", "Income", "Opportunity", "Chance", 
            "Peak", "Hours", "Button", "Click", "Tap", "Go", "Now", "Today",
            "Users", "Connect", "Connects", "Bounce", "Back", "Improve"
        ]
        base_preserved.extend(english_tech_words)
    
    # Moderate code-mixing for Tamil
    elif target_lang == "ta-IN":
        tamil_english_words = [
            "Hey", "Quick", "Update", "Online", "Audio", "Calls", "Active", 
            "Peak", "Hours", "Earn", "Income", "Safe", "Go", "Now", "Users",
            "Chance", "Bounce", "Back", "Improve", "Receive"
        ]
        base_preserved.extend(tamil_english_words)
    
    return base_preserved

def tag_preserved_words(text, target_lang):
    """Enhanced word preservation based on language patterns"""
    enhanced_words = enhance_preserve_words_for_language(target_lang)
    
    for word in enhanced_words:
        # Case-insensitive matching but preserve original case
        text = re.sub(f"\\b{re.escape(word)}\\b", f"[[[{word}]]]", text, flags=re.IGNORECASE)
    
    return text

def untag_preserved_words(text):
    return re.sub(r"\[\[\[(.*?)\]\]\]", r"\1", text)

def calculate_translation_confidence(original, translated, source_lang, target_lang):
    """Calculate a confidence score for the translation (0-1)"""
    if not translated or translated.startswith("❌") or not original:
        return 0.0
    
    confidence = 1.0
    lang_pattern = get_language_specific_settings(target_lang)
    
    # Adjust confidence based on expected patterns
    if target_lang != "en-IN":
        english_words = re.findall(r'\b[A-Za-z]{3,}\b', translated)
        english_ratio = len(english_words) / len(translated.split()) if translated.split() else 0
        
        # Different expectations for different languages
        if lang_pattern["code_mixing"] == "heavy":
            # Hindi/Telugu should have lots of English - penalize if too little
            if english_ratio < 0.2:
                confidence -= 0.3
        elif lang_pattern["code_mixing"] == "moderate":
            # Tamil should have moderate English
            if english_ratio < 0.1 or english_ratio > 0.5:
                confidence -= 0.2
        elif lang_pattern["code_mixing"] == "light":
            # Malayalam/Kannada should have minimal English
            if english_ratio > 0.3:
                confidence -= 0.2
    
    # Penalize dramatic length changes
    length_ratio = len(translated) / len(original) if original else 1
    if length_ratio > 3.0 or length_ratio < 0.3:
        confidence -= 0.2
    
    # Penalize repeated phrases
    words = translated.split()
    if len(words) > 4:
        for i in range(len(words) - 2):
            phrase = " ".join(words[i:i+3])
            if translated.count(phrase) > 1:
                confidence -= 0.3
                break
    
    return max(0.0, min(1.0, confidence))

def analyze_translation_quality(original, translated, source_lang, target_lang):
    """Enhanced quality analysis with language-specific expectations"""
    quality_flags = []
    
    if not translated or translated.startswith("❌"):
        return quality_flags, 0.0
    
    # Calculate confidence score
    confidence = calculate_translation_confidence(original, translated, source_lang, target_lang)
    lang_pattern = get_language_specific_settings(target_lang)
    
    # Language-specific quality checks
    if target_lang != "en-IN":
        english_words = re.findall(r'\b[A-Za-z]{3,}\b', translated)
        english_ratio = len(english_words) / len(translated.split()) if translated.split() else 0
        
        # Check if English retention matches expected pattern
        if lang_pattern["code_mixing"] == "heavy":
            if english_ratio < 0.2:
                quality_flags.append("⚠️ Too little English retained - should preserve more English words for natural code-mixing")
        elif lang_pattern["code_mixing"] == "moderate":
            if english_ratio > 0.5:
                quality_flags.append("⚠️ Too much English retained - should translate more for this language")
        elif lang_pattern["code_mixing"] == "light":
            if english_ratio > 0.3:
                quality_flags.append("⚠️ Too much English retained - should translate more to native script")
    
    # Check dramatic length changes
    if original and translated:
        length_ratio = len(translated) / len(original)
        if length_ratio > 3.0:
            quality_flags.append("📏 Translation much longer than original - please verify completeness")
        elif length_ratio < 0.3:
            quality_flags.append("📏 Translation much shorter than original - may be missing content")
    
    # Check for repeated phrases (potential API glitch)  
    words = translated.split()
    if len(words) > 4:
        for i in range(len(words) - 2):
            phrase = " ".join(words[i:i+3])
            if translated.count(phrase) > 1:
                quality_flags.append("🔄 Repeated phrases detected - may indicate translation error")
                break
    
    return quality_flags, confidence

def prepare_multiline_input(text):
    """Enhanced line break handling"""
    lines = text.strip().split("\n")
    # Use multiple markers to ensure line breaks are preserved
    line_separator = " <LINEBREAK> "
    # Also try alternative markers
    processed_lines = []
    for line in lines:
        if line.strip():
            processed_lines.append(line.strip())
    
    return line_separator.join(processed_lines)

def restore_multiline_output(translated_text, original_text):
    """Improved line break restoration"""
    original_lines = [line.strip() for line in original_text.strip().split("\n") if line.strip()]
    line_separator = " <LINEBREAK> "
    
    # First try our separator
    if line_separator in translated_text:
        translated_lines = translated_text.split(line_separator)
        return "\n".join(translated_lines)
    
    # If that fails, try to detect natural breaking points
    elif len(original_lines) > 1:
        # Try different sentence ending patterns for different languages
        sentence_patterns = [
            r'(?<=[.।!?❌])\s+',  # Standard sentence endings
            r'(?<=[💪🚨🎧🌙💰🔘])\s+',  # Emoji endings (common in your content)
            r'(?<=:)\s+',  # Colon endings
            r'(?<=[?!।])\s*',  # Question/exclamation endings
        ]
        
        for pattern in sentence_patterns:
            sentences = re.split(pattern, translated_text.strip())
            if len(sentences) >= len(original_lines):
                # Try to group sentences to match original line count
                lines_per_group = max(1, len(sentences) // len(original_lines))
                result_lines = []
                
                for i in range(0, len(sentences), lines_per_group):
                    group = sentences[i:i + lines_per_group]
                    result_lines.append(" ".join(group))
                
                if len(result_lines) >= len(original_lines):
                    return "\n".join(result_lines[:len(original_lines)])
    
    # Fallback: return as-is
    return translated_text

def enhance_translation_with_context(text, context_type, audience, formality_level, target_lang):
    """Enhanced context with language-specific instructions"""
    lang_pattern = get_language_specific_settings(target_lang)
    context_instruction = ""
    
    # Base context
    if context_type in CONTEXT_TYPES:
        context_instruction += f"Context: {CONTEXT_TYPES[context_type]}. "
    
    if audience in AUDIENCE_TYPES:
        context_instruction += f"Audience: {AUDIENCE_TYPES[audience]}. "
    
    # Language-specific instructions
    if lang_pattern["code_mixing"] == "heavy":
        context_instruction += "Use heavy code-mixing with English words. Keep technical terms, casual expressions, and simple words in English. Use romanized script. "
    elif lang_pattern["code_mixing"] == "moderate":
        context_instruction += "Use moderate code-mixing. Keep some English words but translate main content to native script. "
    elif lang_pattern["code_mixing"] == "light":
        context_instruction += "Translate most content to native script but keep very simple English words. "
    
    # Formality guidance
    if formality_level <= 2:
        context_instruction += "Use casual, friendly tone with natural conversational style. "
    elif formality_level >= 4:
        context_instruction += "Use formal, respectful tone. "
    
    if context_instruction:
        return f"[INSTRUCTION: {context_instruction}] {text}"
    return text

def translate_text(text, source_lang, target_lang, gender, mode, context_type="", audience="", formality_level=3, regional_variant=""):
    if len(text) > 1000:
        return "❌ Error: Input exceeds 1000 characters."

    # Get language-specific settings
    lang_pattern = get_language_specific_settings(target_lang)
    
    # Override mode based on language pattern if not explicitly set
    if mode == "modern-colloquial":
        mode = lang_pattern["mode"]
    
    # Enhance input with context and language-specific instructions
    enhanced_text = enhance_translation_with_context(text, context_type, audience, formality_level, target_lang)
    prepared_input = prepare_multiline_input(enhanced_text)
    tagged_input = tag_preserved_words(prepared_input, target_lang)

    payload = {
        "input": tagged_input,
        "source_language_code": source_lang,
        "target_language_code": target_lang,
        "mode": mode,
        "speaker_gender": gender,
        "enable_preprocessing": True,
        "numerals_format": "international"
    }

    # Set script based on language pattern
    if lang_pattern["script"] == "roman":
        payload["output_script"] = "roman"
    elif lang_pattern["script"] == "fully-native":
        payload["output_script"] = "fully-native"
    # For "mixed" script, let API decide or don't specify

    headers = {
        "Content-Type": "application/json",
        "api-subscription-key": API_KEY
    }

    response = requests.post("https://api.sarvam.ai/translate", json=payload, headers=headers)

    if response.status_code == 200:
        result_raw = response.json().get("translated_text", "")
        result = untag_preserved_words(result_raw)
        result = restore_multiline_output(result, text)
        
        # Remove context instructions from output if they leaked through
        result = re.sub(r'\[INSTRUCTION:.*?\]\s*', '', result)
        
        return result
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

def check_cultural_sensitivity(text, target_lang):
    """Check for potentially sensitive content"""
    warnings = []
    text_lower = text.lower()
    
    # Religious sensitivity
    if any(word in text_lower for word in ["pork", "beef", "alcohol"]):
        warnings.append("🔍 Contains potentially sensitive content - please review cultural appropriateness")
    
    # Festival timing
    if any(word in text_lower for word in ["christmas", "diwali", "eid", "holi"]):
        warnings.append("📅 Contains festival references - ensure timing is appropriate")
    
    # Financial terms
    if any(word in text_lower for word in ["loan", "debt", "payment", "money"]):
        warnings.append("💰 Contains financial terms - ensure compliance with regulations")
    
    return warnings

# -------------------- STREAMLIT UI -------------------- #
st.title("🎯 FRND Enhanced Translator")
st.markdown("*Language-specific patterns for natural code-mixing and context preservation*")

# Language pattern info
with st.expander("📋 Language-Specific Patterns"):
    st.markdown("""
    **Hindi & Telugu**: Heavy code-mixing with romanized script (e.g., "abhi online ho jao")
    
    **Tamil**: Moderate code-mixing with Tamil script + English words (e.g., "நீங்க online போங்க") 
    
    **Malayalam & Kannada**: Light code-mixing with native script (mostly translated)
    """)

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("📝 Input Text")
    text = st.text_area("Enter text to translate:", height=200)
    
    # Cultural sensitivity check
    if text:
        target_lang_code = st.session_state.get('target_lang', 'hi-IN')
        sensitivity_warnings = check_cultural_sensitivity(text, target_lang_code)
        for warning in sensitivity_warnings:
            st.warning(warning)

with col2:
    st.subheader("⚙️ Quality Settings")
    
    # Basic language settings
    col_lang1, col_lang2 = st.columns(2)
    with col_lang1:
        source_ui = st.selectbox("From:", list(LANG_MAP.keys()), index=10)
    with col_lang2:
        target_ui = st.selectbox("To:", list(LANG_MAP.keys()), index=0)
        st.session_state.target_lang = LANG_MAP[target_ui]
    
    # Show expected pattern for selected language
    if target_ui != "English":
        lang_pattern = get_language_specific_settings(LANG_MAP[target_ui])
        st.info(f"📋 **{target_ui} Pattern**: {lang_pattern['code_mixing'].title()} code-mixing, {lang_pattern['script']} script")
    
    # Quality enhancement settings
    st.markdown("**Context & Audience**")
    context_type = st.selectbox("Message Type:", [""] + list(CONTEXT_TYPES.keys()))
    audience = st.selectbox("Target Audience:", [""] + list(AUDIENCE_TYPES.keys()))
    
    formality_level = st.slider("Formality Level:", 1, 5, 2, 
        help="1=Very Casual, 3=Neutral, 5=Very Formal")
    
    # Regional variant (if available)
    target_code = LANG_MAP[target_ui]
    if target_code in REGIONAL_VARIANTS:
        regional_variant = st.selectbox(f"{target_ui} Variant:", 
            ["Standard"] + REGIONAL_VARIANTS[target_code])
    else:
        regional_variant = ""
    
    st.markdown("**Translation Style**")
    col_gender, col_mode = st.columns(2)
    with col_gender:
        gender = st.selectbox("Gender:", ["Male", "Female"])
    with col_mode:
        mode_ui = st.selectbox("Style:", list(MODE_OPTIONS.keys()), index=0)

# Translate button
if st.button("🔄 Translate with Enhanced Patterns", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter text to translate.")
    else:
        with st.spinner("Translating with language-specific patterns..."):
            src = LANG_MAP[source_ui]
            tgt = LANG_MAP[target_ui]
            selected_mode = MODE_OPTIONS[mode_ui]
            
            result = translate_text(
                text.strip(), src, tgt, gender, selected_mode,
                context_type, audience, formality_level, regional_variant
            )
            
            st.session_state.last_translation = result
            st.session_state.original_text = text
            st.session_state.source_lang = source_ui
            st.session_state.target_lang_ui = target_ui

# Display results with quality analysis
if 'last_translation' in st.session_state:
    st.divider()
    st.subheader("📋 Translation Result")
    
    result_text = st.session_state.last_translation
    st.text_area("Translated Output:", value=result_text, height=150)
    
    # Quality analysis with confidence score
    if not result_text.startswith("❌"):
        quality_flags, confidence_score = analyze_translation_quality(
            st.session_state.original_text, 
            result_text, 
            LANG_MAP[st.session_state.source_lang], 
            LANG_MAP[st.session_state.target_lang_ui]
        )
        
        # Display confidence score
        st.subheader("🎯 Translation Quality")
        col_conf1, col_conf2 = st.columns(2)
        with col_conf1:
            if confidence_score >= 0.8:
                st.success(f"✅ High Confidence: {confidence_score:.1%}")
            elif confidence_score >= 0.7:
                st.info(f"📊 Good Confidence: {confidence_score:.1%}")
            else:
                st.error(f"⚠️ Low Confidence: {confidence_score:.1%}")
        
        with col_conf2:
            if confidence_score < 0.7:
                st.error("🚨 **REVIEW REQUIRED** - Translation may need manual review")
        
        # Show quality flags if any
        if quality_flags:
            st.subheader("🔍 Quality Analysis")
            for flag in quality_flags:
                st.info(flag)
        elif confidence_score >= 0.7:
            st.success("✅ Translation meets quality standards")
    
    # Action buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        st.download_button("📥 Download", result_text, 
            file_name=f"translation_{st.session_state.target_lang_ui.lower()}.txt")
    with col_btn2:
        if st.button("🔄 Retranslate"):
            st.rerun()
    with col_btn3:
        if st.button("⭐ Mark as Approved"):
            st.success("Translation approved!")

# Help section
with st.expander("ℹ️ Enhanced Features Guide"):
    st.markdown("""
    **Language-Specific Patterns**: Automatically optimizes code-mixing and script usage per language
    
    **Enhanced Line Breaks**: Better preservation of text structure and formatting
    
    **Context Preservation**: Improved handling of meaning and cultural context
    
    **Confidence Scoring**: Validates translation quality against expected patterns
    
    **Smart Word Preservation**: Language-aware preservation of English terms
    """)

st.markdown("---")
st.markdown("*FRND Enhanced Translator • Optimized for Natural Code-Mixing Patterns*")
