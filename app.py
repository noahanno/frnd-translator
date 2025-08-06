import os
import streamlit as st
from dotenv import load_dotenv
import requests
import re
import emoji

# Load environment variables
load_dotenv()
API_KEY = os.getenv("SARVAM_API_KEY", st.secrets.get("SARVAM_API_KEY", ""))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))

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

# -------------------- ISSUE-SPECIFIC OPTIMIZATION -------------------- #

# Issue-based corrections and improvements (Applied across ALL languages)
TRANSLATION_OPTIMIZATIONS = {
    "universal": {
        "sentence_completion_hints": [
            "friend", "interesting friend", "new friendship", "make friends",
            "find friends", "become friends", "first step", "today", 
            "take action", "start now", "lighthearted call", "catchy"
        ],
        "brand_protection_fixes": {
            r"\[\[+([^\[\]]*)\]\]+": r"\1",  # Remove multiple brackets
            r"\{\{+([^\{\}]*)\}\}+": r"\1",  # Remove multiple braces
            r"\[+FRND\]+": "FRND",           # Clean FRND specifically
            r"\{+FRND\}+": "FRND",           # Clean FRND specifically
            r"\[+Team\s*FRND\]+": "Team FRND",  # Clean Team FRND
        },
        "catchy_phrases_enhancement": {
            "What is the scene": {
                "hi-IN": "Scene kya hai",
                "ta-IN": "Scene என்னங்க",
                "te-IN": "Scene entante",
                "ml-IN": "എന്താണ് scene",
                "kn-IN": "Scene ಏನು"
            },
            "Take the first step": {
                "hi-IN": "Pehla step lo",
                "ta-IN": "First step எடுங்க", 
                "te-IN": "Modati step teeskondi",
                "ml-IN": "ആദ്യ step എടുക്കൂ",
                "kn-IN": "ಮೊದಲ step ತೆಗೆದುಕೊಳ್ಳಿ"
            },
            "lighthearted call": {
                "hi-IN": "casual call",
                "ta-IN": "lighthearted-ஆ call",
                "te-IN": "casual ga call",
                "ml-IN": "സുഖമായി call",
                "kn-IN": "ಸುಲಭವಾಗಿ call"
            }
        }
    }
}

# -------------------- ENHANCED HELPER FUNCTIONS -------------------- #

def preprocess_input_for_completeness(text, target_lang):
    """Add hints to ensure complete translation across ALL languages"""
    
    # Universal completion hints
    hints = TRANSLATION_OPTIMIZATIONS["universal"]["sentence_completion_hints"]
    
    # Check if text contains elements that often get missed
    missing_elements = []
    for hint in hints:
        if hint.lower() in text.lower():
            missing_elements.append(hint)
    
    if missing_elements:
        # Add subtle instruction to include all elements
        instruction = f"[Translate completely including: {', '.join(missing_elements)}] "
        return instruction + text
    
    return text

def fix_brand_name_issues(text, target_lang):
    """Fix brand name formatting issues across ALL languages"""
    
    # Apply universal brand protection fixes
    fixes = TRANSLATION_OPTIMIZATIONS["universal"]["brand_protection_fixes"]
    for pattern, replacement in fixes.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def fix_formatting_issues(text, target_lang):
    """Fix unnecessary spacing and cleanup across ALL languages"""
    
    # General formatting cleanup only (no bold text removal)
    text = re.sub(r'\s+', ' ', text)                # Clean extra spaces
    text = text.strip()                             # Remove leading/trailing spaces
    
    return text

def enhance_catchy_phrases(text, target_lang):
    """Improve translation of catchy/marketing phrases across ALL languages"""
    
    catchy_phrases = TRANSLATION_OPTIMIZATIONS["universal"]["catchy_phrases_enhancement"]
    
    for phrase, translations in catchy_phrases.items():
        if phrase.lower() in text.lower() and target_lang in translations:
            # Replace with better translations for catchy phrases
            text = re.sub(re.escape(phrase), translations[target_lang], text, flags=re.IGNORECASE)
    
    return text

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
    """Calculate confidence score for translation with universal issue checks"""
    if not translated or translated.startswith("❌") or not original:
        return 0.0
    
    confidence = 1.0
    
    # Universal issue checks (applied to all languages)
    
    # Check for bracket issues (any language)
    if re.search(r'\[+[^\[\]]*\]+', translated):
        confidence -= 0.3
    
    # Check for incomplete translations (any language)
    original_sentences = len(re.findall(r'[.!?]+', original))
    translated_sentences = len(re.findall(r'[.!?।]+', translated))
    if original_sentences > translated_sentences + 1:
        confidence -= 0.4
    
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

# -------------------- CHATGPT INTEGRATION -------------------- #

def get_chatgpt_translation(text, target_lang, source_lang="en-IN"):
    """Get translation from ChatGPT for comparison"""
    
    if not OPENAI_API_KEY:
        return None, "OpenAI API key not found"
    
    # Language mapping for ChatGPT
    lang_names = {
        "hi-IN": "Hindi with Roman script and English code-mixing (like: 'weekend ON ho chuka hai')",
        "ta-IN": "Tamil script with selective English words (like: 'Saturday – weekend OFFICIALLY ON!')",
        "te-IN": "Telugu with Roman script and English code-mixing (like: 'weekend officially ON lo undhi')",
        "ml-IN": "Malayalam script with simple English terms preserved",
        "kn-IN": "Kannada script with simple English terms preserved"
    }
    
    target_lang_instruction = lang_names.get(target_lang, "the target language")
    
    prompt = f"""Translate this English text to {target_lang_instruction}:

"{text}"

Keep the translation natural and engaging, preserving brand names like FRND, and maintain the style shown in the examples."""

    try:
        # Updated headers and payload for current OpenAI API
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",  # Using cheaper model first
            "messages": [
                {"role": "system", "content": "You are a professional translator specializing in Indian languages with natural code-mixing patterns."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.3
        }
        
        # Correct OpenAI API endpoint
        response = requests.post("https://api.openai.com/v1/chat/completions", 
                               headers=headers, 
                               json=payload, 
                               timeout=30)
        
        # Debug information
        if response.status_code != 200:
            return None, f"OpenAI API Error: {response.status_code} - {response.text[:200]}"
        
        try:
            result = response.json()
            if "choices" not in result or len(result["choices"]) == 0:
                return None, f"No translation returned: {result}"
            
            translation = result["choices"][0]["message"]["content"].strip()
            return translation, None
            
        except KeyError as ke:
            return None, f"Response parsing error: {ke} - Response: {response.text[:200]}"
            
    except requests.exceptions.Timeout:
        return None, "OpenAI API timeout - try again"
    except requests.exceptions.ConnectionError:
        return None, "Connection error - check internet"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

def calculate_chatgpt_confidence(original, translated, target_lang):
    """Calculate confidence score for ChatGPT translation"""
    if not translated:
        return 0.0
    
    confidence = 1.0
    
    # Check for appropriate code-mixing patterns
    if target_lang in ["hi-IN", "te-IN"]:
        # Should have good English mixing
        english_words = re.findall(r'\b[A-Za-z]{3,}\b', translated)
        english_ratio = len(english_words) / len(translated.split()) if translated.split() else 0
        if english_ratio < 0.2:  # Too little English for code-mixed languages
            confidence -= 0.2
    
    # Check length ratio
    length_ratio = len(translated) / len(original) if original else 1
    if length_ratio > 3.0 or length_ratio < 0.3:
        confidence -= 0.2
    
    # Check for brand name preservation
    if "FRND" in original.upper() and "FRND" not in translated:
        confidence -= 0.3
    
    # Check sentence completeness
    original_sentences = len(re.findall(r'[.!?]+', original))
    translated_sentences = len(re.findall(r'[.!?।]+', translated))
    if original_sentences > translated_sentences + 1:
        confidence -= 0.3
    
    return max(0.0, min(1.0, confidence))

def analyze_translation_quality(original, translated, source_lang, target_lang):
    """Enhanced quality analysis with universal issue detection"""
    quality_flags = []
    
    if not translated or translated.startswith("❌"):
        return quality_flags, 0.0
    
    confidence = calculate_translation_confidence(original, translated, source_lang, target_lang)
    
    # Universal quality checks (applied to ALL languages)
    if re.search(r'\[+[^\[\]]*\]+', translated):
        quality_flags.append("🔧 Brand name formatting issue detected - brackets around text")
    
    # Check for incomplete sentence translation
    original_sentences = len(re.findall(r'[.!?]+', original))
    translated_sentences = len(re.findall(r'[.!?।]+', translated))
    if original_sentences > translated_sentences + 1:
        quality_flags.append("📝 Possible incomplete translation - missing sentences")
    
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
    # Get language-specific settings
    lang_pattern = get_language_specific_settings(target_lang)
    
    # Override mode based on language pattern
    if mode == "modern-colloquial":
        mode = lang_pattern["mode"]
    
    # ENHANCED INPUT PREPROCESSING
    # 1. Add completeness hints
    enhanced_text = preprocess_input_for_completeness(text, target_lang)
    
    # 2. Enhance catchy phrases
    enhanced_text = enhance_catchy_phrases(enhanced_text, target_lang)
    
    # 3. Prepare for API
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
        
        # ENHANCED OUTPUT POST-PROCESSING
        # 1. Clean leaked instructions
        result = re.sub(r'\[INSTRUCTION:.*?\]\s*', '', result)
        result = re.sub(r'\[INST:.*?\]\s*', '', result)
        result = re.sub(r'\[Translate completely including:.*?\]\s*', '', result)
        
        # 2. Fix brand name issues
        result = fix_brand_name_issues(result, target_lang)
        
        # 3. Fix formatting issues
        result = fix_formatting_issues(result, target_lang)
        
        # 4. Apply universal language fixes (no specific language restrictions)
        # Apply universal fixes - no need for language-specific checks anymore
        
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
st.title("🎯 FRND Enhanced Translator")
st.markdown("*Issue-optimized translations with smart corrections*")

# Quality improvements info
with st.expander("🔧 Universal Quality Improvements"):
    st.markdown("""
    **Improvements Applied to ALL Languages:**
    - 🎯 **Complete Translations**: Ensures all parts including "interesting friend", "first step" are translated
    - 🔧 **Brand Protection**: Automatic removal of brackets around FRND, Team FRND across all languages
    - 📝 **Sentence Completion**: Enhanced detection and prevention of missing sentences
    - 🎨 **Catchy Phrase Enhancement**: Better translation of marketing phrases across all languages
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
    
    st.markdown("**Translation Options**")
    
    # Add ChatGPT comparison toggle
    enable_chatgpt = st.checkbox("🤖 Enable ChatGPT Comparison", 
                                help="Get ChatGPT translation for quality comparison")
    
    col_gender, col_mode = st.columns(2)
    with col_gender:
        gender = st.selectbox("Gender:", ["Male", "Female"])
    with col_mode:
        mode_ui = st.selectbox("Style:", list(MODE_OPTIONS.keys()), index=3)  # Default to Blended

# Translate button
if st.button("🔄 Translate with Enhanced Quality", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter text to translate.")
    else:
        with st.spinner("Translating with issue-specific optimizations..."):
            src = LANG_MAP[source_ui]
            tgt = LANG_MAP[target_ui]
            selected_mode = MODE_OPTIONS[mode_ui]
            
            # Get Sarvam translation
            sarvam_result = translate_text(
                text.strip(), src, tgt, gender, selected_mode,
                context_type, audience, formality_level
            )
            
            # Get ChatGPT translation if enabled
            chatgpt_result = None
            chatgpt_error = None
            if enable_chatgpt:
                with st.spinner("Getting ChatGPT comparison..."):
                    chatgpt_result, chatgpt_error = get_chatgpt_translation(text.strip(), tgt, src)
            
            # Store results
            st.session_state.last_translation = sarvam_result
            st.session_state.chatgpt_translation = chatgpt_result
            st.session_state.chatgpt_error = chatgpt_error
            st.session_state.original_text = text
            st.session_state.source_lang = source_ui
            st.session_state.target_lang_ui = target_ui
            st.session_state.enable_chatgpt = enable_chatgpt

# Display results with enhanced quality analysis
if 'last_translation' in st.session_state:
    st.divider()
    st.subheader("📋 Translation Results")
    
    # Create columns for side-by-side comparison if ChatGPT is enabled
    if st.session_state.get('enable_chatgpt', False) and st.session_state.get('chatgpt_translation'):
        col_sarvam, col_chatgpt = st.columns(2)
        
        with col_sarvam:
            st.markdown("### 🎯 Sarvam Translation")
            sarvam_result = st.session_state.last_translation
            st.text_area("Sarvam Output:", value=sarvam_result, height=120, key="sarvam_output")
            
        with col_chatgpt:
            st.markdown("### 🤖 ChatGPT Translation")
            chatgpt_result = st.session_state.chatgpt_translation
            st.text_area("ChatGPT Output:", value=chatgpt_result, height=120, key="chatgpt_output")
    else:
        # Single translation display
        sarvam_result = st.session_state.last_translation
        st.text_area("Sarvam Translation:", value=sarvam_result, height=150)
        
        # Show ChatGPT error if any
        if st.session_state.get('enable_chatgpt', False) and st.session_state.get('chatgpt_error'):
            st.error(f"ChatGPT Error: {st.session_state.chatgpt_error}")
    
    # Quality Analysis
    if not sarvam_result.startswith("❌"):
        # Calculate confidence scores
        sarvam_quality_flags, sarvam_confidence = analyze_translation_quality(
            st.session_state.original_text, 
            sarvam_result, 
            LANG_MAP[st.session_state.source_lang], 
            LANG_MAP[st.session_state.target_lang_ui]
        )
        
        # Calculate ChatGPT confidence if available
        chatgpt_confidence = 0.0
        if st.session_state.get('chatgpt_translation'):
            chatgpt_confidence = calculate_chatgpt_confidence(
                st.session_state.original_text,
                st.session_state.chatgpt_translation,
                LANG_MAP[st.session_state.target_lang_ui]
            )
        
        # Display confidence scores
        st.subheader("🎯 Translation Quality Comparison")
        
        if st.session_state.get('chatgpt_translation'):
            col_sarvam_conf, col_chatgpt_conf = st.columns(2)
            
            with col_sarvam_conf:
                st.markdown("**Sarvam Confidence**")
                if sarvam_confidence >= 0.8:
                    st.success(f"✅ {sarvam_confidence:.1%}")
                elif sarvam_confidence >= 0.7:
                    st.info(f"📊 {sarvam_confidence:.1%}")
                else:
                    st.error(f"⚠️ {sarvam_confidence:.1%}")
            
            with col_chatgpt_conf:
                st.markdown("**ChatGPT Confidence**")
                if chatgpt_confidence >= 0.8:
                    st.success(f"✅ {chatgpt_confidence:.1%}")
                elif chatgpt_confidence >= 0.7:
                    st.info(f"📊 {chatgpt_confidence:.1%}")
                else:
                    st.error(f"⚠️ {chatgpt_confidence:.1%}")
            
            # Winner indication
            st.markdown("---")
            if sarvam_confidence > chatgpt_confidence:
                st.success("🏆 **Sarvam wins this round!**")
            elif chatgpt_confidence > sarvam_confidence:
                st.info("🏆 **ChatGPT wins this round!**")
            else:
                st.warning("🤝 **It's a tie!**")
                
        else:
            # Single confidence display
            if sarvam_confidence >= 0.8:
                st.success(f"✅ Sarvam Confidence: {sarvam_confidence:.1%}")
            elif sarvam_confidence >= 0.7:
                st.info(f"📊 Sarvam Confidence: {sarvam_confidence:.1%}")
            else:
                st.error(f"⚠️ Sarvam Confidence: {sarvam_confidence:.1%}")
                st.error("🚨 **REVIEW REQUIRED** - Translation may need manual review")
        
        # Show quality flags if any
        if sarvam_quality_flags:
            st.subheader("🔍 Sarvam Quality Analysis")
            for flag in sarvam_quality_flags:
                st.info(flag)
        elif sarvam_confidence >= 0.7:
            st.success("✅ Sarvam translation meets enhanced quality standards")
    
    # Action buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        # Download the better translation
        if st.session_state.get('chatgpt_translation'):
            sarvam_conf = analyze_translation_quality(
                st.session_state.original_text, 
                st.session_state.last_translation, 
                LANG_MAP[st.session_state.source_lang], 
                LANG_MAP[st.session_state.target_lang_ui]
            )[1]
            chatgpt_conf = calculate_chatgpt_confidence(
                st.session_state.original_text,
                st.session_state.chatgpt_translation,
                LANG_MAP[st.session_state.target_lang_ui]
            )
            better_translation = st.session_state.chatgpt_translation if chatgpt_conf > sarvam_conf else st.session_state.last_translation
        else:
            better_translation = st.session_state.last_translation
            
        st.download_button("📥 Download Best", better_translation, 
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
    **Universal Optimizations**: 
    - **Complete Translations**: Ensures all sentence parts are translated across all languages
    - **Brand Protection**: Prevents formatting issues with FRND brand name in any language
    - **Sentence Completion**: Advanced detection of incomplete translations
    - **Catchy Phrase Enhancement**: Better translation of marketing phrases universally
    - **Quality Detection**: Universal detection of common translation issues
    
    **Applied to All Languages**:
    - **Hindi, Tamil, Telugu, Malayalam, Kannada**: All benefit from the same quality improvements
    - **Consistent Quality**: Same high standards across all target languages
    """)

st.markdown("---")
st.markdown("*FRND Enhanced Translator • Issue-Optimized Quality*")
