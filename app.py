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
        "script": "roman",
        "mode": "code-mixed"
    },
    "te-IN": {
        "script": "roman", 
        "mode": "code-mixed"
    },
    "ta-IN": {
        "script": "mixed",
        "mode": "modern-colloquial"
    },
    "ml-IN": {
        "script": "fully-native",
        "mode": "formal"
    },
    "kn-IN": {
        "script": "fully-native",
        "mode": "formal"
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
    "Marketing/Promotional": "Use engaging, persuasive language",
    "Technical Support": "Use clear, helpful, problem-solving tone",
    "Payment/Financial": "Use formal, trustworthy language", 
    "Festival/Cultural": "Use warm, celebratory, culturally appropriate tone",
    "Customer Service": "Use polite, empathetic, solution-oriented tone",
    "Urgent/Emergency": "Use direct, clear, action-oriented language"
}

AUDIENCE_TYPES = {
    "Young Adults (18-30)": "casual, trendy expressions",
    "Middle-aged (30-50)": "respectful, professional tone",
    "Senior Citizens (50+)": "formal, respectful, clear language", 
    "Business Professionals": "formal, professional terminology"
}

# Regional variations - removed from UI but kept for future use
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

# -------------------- HELPER FUNCTIONS -------------------- #
def get_language_specific_settings(target_lang):
    """Get optimized settings for each language"""
    if target_lang in LANGUAGE_PATTERNS:
        return LANGUAGE_PATTERNS[target_lang]
    else:
        return {
            "script": "roman",
            "mode": "modern-colloquial"
        }

def tag_preserved_words(text):
    """Tag preserved words for API"""
    for word in PRESERVE_WORDS:
        text = re.sub(f"\\b{re.escape(word)}\\b", f"[[[{word}]]]", text, flags=re.IGNORECASE)
    return text

def untag_preserved_words(text):
    """Remove tags from preserved words"""
    return re.sub(r"\[\[\[(.*?)\]\]\]", r"\1", text)

def prepare_multiline_input(text):
    """Prepare multiline text for API"""
    lines = text.strip().split("\n")
    line_separator = " <LINEBREAK> "
    processed_lines = []
    for line in lines:
        if line.strip():
            processed_lines.append(line.strip())
    return line_separator.join(processed_lines)

def restore_multiline_output(translated_text, original_text):
    """Restore line breaks in output"""
    original_lines = [line.strip() for line in original_text.strip().split("\n") if line.strip()]
    line_separator = " <LINEBREAK> "
    
    # First try our separator
    if line_separator in translated_text:
        translated_lines = translated_text.split(line_separator)
        return "\n".join(translated_lines)
    
    # If that fails, try to detect natural breaking points
    elif len(original_lines) > 1:
        sentence_patterns = [
            r'(?<=[.।!?❌])\s+',
            r'(?<=[💪🚨🎧🌙💰🔘])\s+',
            r'(?<=[?!।])\s*',
        ]
        
        for pattern in sentence_patterns:
            sentences = re.split(pattern, translated_text.strip())
            if len(sentences) >= len(original_lines):
                lines_per_group = max(1, len(sentences) // len(original_lines))
                result_lines = []
                
                for i in range(0, len(sentences), lines_per_group):
                    group = sentences[i:i + lines_per_group]
                    result_lines.append(" ".join(group))
                
                if len(result_lines) >= len(original_lines):
                    return "\n".join(result_lines[:len(original_lines)])
    
    return translated_text

def calculate_translation_confidence(original, translated, source_lang, target_lang):
    """Calculate confidence score for translation"""
    if not translated or translated.startswith("❌") or not original:
        return 0.0
    
    confidence = 1.0
    
    # Check length ratio
    length_ratio = len(translated) / len(original) if original else 1
    if length_ratio > 3.0 or length_ratio < 0.3:
        confidence -= 0.2
    
    # Check for repeated phrases
    words = translated.split()
    if len(words) > 4:
        for i in range(len(words) - 2):
            phrase = " ".join(words[i:i+3])
            if translated.count(phrase) > 1:
                confidence -= 0.3
                break
    
    return max(0.0, min(1.0, confidence))

def analyze_translation_quality(original, translated, source_lang, target_lang):
    """Analyze translation quality"""
    quality_flags = []
    
    if not translated or translated.startswith("❌"):
        return quality_flags, 0.0
    
    confidence = calculate_translation_confidence(original, translated, source_lang, target_lang)
    
    # Check dramatic length changes
    if original and translated:
        length_ratio = len(translated) / len(original)
        if length_ratio > 3.0:
            quality_flags.append("📏 Translation much longer than original - please verify completeness")
        elif length_ratio < 0.3:
            quality_flags.append("📏 Translation much shorter than original - may be missing content")
    
    # Check for repeated phrases
    words = translated.split()
    if len(words) > 4:
        for i in range(len(words) - 2):
            phrase = " ".join(words[i:i+3])
            if translated.count(phrase) > 1:
                quality_flags.append("🔄 Repeated phrases detected - may indicate translation error")
                break
    
    return quality_flags, confidence

def translate_text(text, source_lang, target_lang, gender, mode, context_type="", audience="", formality_level=3):
    # REMOVED CHARACTER LIMIT
    
    # Get language-specific settings
    lang_pattern = get_language_specific_settings(target_lang)
    
    # Override mode based on language pattern
    if mode == "modern-colloquial":
        mode = lang_pattern["mode"]
    
    # CLEAN INPUT - NO CONTEXT INSTRUCTIONS ADDED
    prepared_input = prepare_multiline_input(text)
    tagged_input = tag_preserved_words(prepared_input)

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

    headers = {
        "Content-Type": "application/json",
        "api-subscription-key": API_KEY
    }

    response = requests.post("https://api.sarvam.ai/translate", json=payload, headers=headers)

    if response.status_code == 200:
        result_raw = response.json().get("translated_text", "")
        result = untag_preserved_words(result_raw)
        result = restore_multiline_output(result, text)
        
        # CLEAN OUTPUT - Remove any leaked instructions
        result = re.sub(r'\[INSTRUCTION:.*?\]\s*', '', result)
        result = re.sub(r'\[INST:.*?\]\s*', '', result)
        
        return result
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

def check_cultural_sensitivity(text, target_lang):
    """Check for potentially sensitive content"""
    warnings = []
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["pork", "beef", "alcohol"]):
        warnings.append("🔍 Contains potentially sensitive content - please review cultural appropriateness")
    
    if any(word in text_lower for word in ["christmas", "diwali", "eid", "holi"]):
        warnings.append("📅 Contains festival references - ensure timing is appropriate")
    
    if any(word in text_lower for word in ["loan", "debt", "payment", "money"]):
        warnings.append("💰 Contains financial terms - ensure compliance with regulations")
    
    return warnings

# -------------------- STREAMLIT UI -------------------- #
st.title("🎯 FRND Quality Translator")
st.markdown("*Clean translations with language-specific patterns*")

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
    st.subheader("⚙️ Settings")
    
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
        st.info(f"📋 **{target_ui}**: {lang_pattern['script']} script, {lang_pattern['mode']} style")
    
    # Quality enhancement settings
    st.markdown("**Context & Audience**")
    context_type = st.selectbox("Message Type:", [""] + list(CONTEXT_TYPES.keys()))
    audience = st.selectbox("Target Audience:", [""] + list(AUDIENCE_TYPES.keys()))
    
    formality_level = st.slider("Formality Level:", 1, 5, 2, 
        help="1=Very Casual, 3=Neutral, 5=Very Formal")
    
    # Regional variant removed - not needed
    
    st.markdown("**Translation Style**")
    col_gender, col_mode = st.columns(2)
    with col_gender:
        gender = st.selectbox("Gender:", ["Male", "Female"])
    with col_mode:
        mode_ui = st.selectbox("Style:", list(MODE_OPTIONS.keys()), index=3)  # Default to Blended

# Translate button
if st.button("🔄 Translate", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter text to translate.")
    else:
        with st.spinner("Translating..."):
            src = LANG_MAP[source_ui]
            tgt = LANG_MAP[target_ui]
            selected_mode = MODE_OPTIONS[mode_ui]
            
            result = translate_text(
                text.strip(), src, tgt, gender, selected_mode,
                context_type, audience, formality_level
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
with st.expander("ℹ️ Features Guide"):
    st.markdown("""
    **Language-Specific Patterns**: 
    - Hindi & Telugu: Roman script with heavy code-mixing
    - Tamil: Mixed script with moderate English
    - Malayalam & Kannada: Native script with minimal English
    
    **Clean Output**: No unwanted instructions in translations
    
    **No Character Limits**: Translate texts of any length
    
    **Quality Scoring**: Confidence validation for translations
    """)

st.markdown("---")
st.markdown("*FRND Quality Translator • Clean & Natural Translations*")
