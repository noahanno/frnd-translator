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
SOUTH_INDIAN = {"ta-IN", "te-IN", "ml-IN", "kn-IN", "or-IN"}
DEFAULT_SCRIPT = {
    "roman": {"hi-IN", "pa-IN", "bn-IN", "mr-IN", "gu-IN"},
    "fully-native": SOUTH_INDIAN
}

# Enhanced mode options with quality focus
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

# -------------------- QUALITY HELPER FUNCTIONS -------------------- #
def tag_preserved_words(text):
    for word in PRESERVE_WORDS:
        text = re.sub(f"\\b{re.escape(word)}\\b", f"[[[{word}]]]", text)
    return text

def untag_preserved_words(text):
    return re.sub(r"\[\[\[(.*?)\]\]\]", r"\1", text)

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

def analyze_translation_quality(original, translated, source_lang, target_lang):
    """Analyze potential translation quality issues"""
    quality_flags = []
    
    if not translated or translated.startswith("❌"):
        return quality_flags
    
    # Check for excessive English retention in non-English targets
    if target_lang != "en-IN":
        english_words = re.findall(r'\b[A-Za-z]{3,}\b', translated)
        english_ratio = len(english_words) / len(translated.split()) if translated.split() else 0
        
        if english_ratio > 0.3:
            quality_flags.append("⚠️ High English word retention - may need review for naturalness")
    
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
    
    return quality_flags

def prepare_multiline_input(text):
    lines = text.strip().split("\n")
    line_separator = " <LINEBREAK> "
    return line_separator.join([line.strip() for line in lines if line.strip()])

def restore_multiline_output(translated_text, original_text):
    original_lines = [line.strip() for line in original_text.strip().split("\n") if line.strip()]
    line_separator = " <LINEBREAK> "
    
    if line_separator in translated_text:
        translated_lines = translated_text.split(line_separator)
        return "\n".join(translated_lines)
    elif len(original_lines) > 1:
        sentences = re.split(r'(?<=[.।!?])\s+', translated_text.strip())
        if len(sentences) >= len(original_lines):
            lines_per_group = len(sentences) // len(original_lines)
            result_lines = []
            for i in range(0, len(sentences), max(1, lines_per_group)):
                group = sentences[i:i + lines_per_group]
                result_lines.append(" ".join(group))
            return "\n".join(result_lines[:len(original_lines)])
    return translated_text

def enhance_translation_with_context(text, context_type, audience, formality_level):
    """Add context-aware instructions to improve translation quality"""
    context_instruction = ""
    
    if context_type in CONTEXT_TYPES:
        context_instruction += f"Context: {CONTEXT_TYPES[context_type]}. "
    
    if audience in AUDIENCE_TYPES:
        context_instruction += f"Audience: {AUDIENCE_TYPES[audience]}. "
    
    if formality_level <= 2:
        context_instruction += "Use casual, friendly tone. "
    elif formality_level >= 4:
        context_instruction += "Use formal, respectful tone. "
    
    if context_instruction:
        return f"[INSTRUCTION: {context_instruction}] {text}"
    return text

def translate_text(text, source_lang, target_lang, gender, mode, context_type="", audience="", formality_level=3, regional_variant=""):
    if len(text) > 1000:
        return "❌ Error: Input exceeds 1000 characters."

    # Enhance input with context
    enhanced_text = enhance_translation_with_context(text, context_type, audience, formality_level)
    prepared_input = prepare_multiline_input(enhanced_text)
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

    # Handle script preferences
    if target_lang in DEFAULT_SCRIPT["roman"]:
        payload["output_script"] = "roman"
    elif target_lang in DEFAULT_SCRIPT["fully-native"]:
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
        
        # Remove context instructions from output if they leaked through
        result = re.sub(r'\[INSTRUCTION:.*?\]\s*', '', result)
        
        return result
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# -------------------- STREAMLIT UI -------------------- #
st.title("🎯 FRND Quality-Focused Translator")
st.markdown("*Enhanced translation with cultural awareness and quality controls*")

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
    
    # Quality enhancement settings
    st.markdown("**Context & Audience**")
    context_type = st.selectbox("Message Type:", [""] + list(CONTEXT_TYPES.keys()))
    audience = st.selectbox("Target Audience:", [""] + list(AUDIENCE_TYPES.keys()))
    
    formality_level = st.slider("Formality Level:", 1, 5, 3, 
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
if st.button("🔄 Translate with Quality Check", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter text to translate.")
    else:
        with st.spinner("Translating with quality analysis..."):
            src = LANG_MAP[source_ui]
            tgt = LANG_MAP[target_ui]
            selected_mode = MODE_OPTIONS[mode_ui]
            
            result = translate_text(
                text.strip(), src, tgt, gender, selected_mode,
                context_type, audience, formality_level, regional_variant
            )
            
            st.session_state.last_translation = result
            st.session_state.original_text = text

# Display results with quality analysis
if 'last_translation' in st.session_state:
    st.divider()
    st.subheader("📋 Translation Result")
    
    result_text = st.session_state.last_translation
    st.text_area("Translated Output:", value=result_text, height=150)
    
    # Quality analysis
    if not result_text.startswith("❌"):
        quality_flags = analyze_translation_quality(
            st.session_state.original_text, 
            result_text, 
            LANG_MAP[source_ui], 
            LANG_MAP[target_ui]
        )
        
        if quality_flags:
            st.subheader("🔍 Quality Analysis")
            for flag in quality_flags:
                st.info(flag)
        else:
            st.success("✅ No quality issues detected")
    
    # Action buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        st.download_button("📥 Download", result_text, 
            file_name=f"translation_{target_ui.lower()}.txt")
    with col_btn2:
        if st.button("🔄 Retranslate"):
            st.rerun()
    with col_btn3:
        if st.button("⭐ Mark as Approved"):
            st.success("Translation approved!")

# Help section
with st.expander("ℹ️ Quality Features Guide"):
    st.markdown("""
    **Context Types:** Choose the type of message to get contextually appropriate translations
    
    **Audience:** Select your target demographic for age-appropriate language
    
    **Formality Level:** Control how formal or casual the translation should be
    
    **Regional Variants:** Choose specific regional dialects when available
    
    **Quality Analysis:** Automatic detection of potential translation issues
    
    **Cultural Sensitivity:** Warnings for potentially sensitive content
    """)

st.markdown("---")
st.markdown("*FRND Quality Translator • Advanced AI with Cultural Intelligence*")