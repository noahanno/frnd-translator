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
    
    # Apply universal brand protection fixes - more aggressive cleaning
    fixes = {
        r"\[\[\[+([^\[\]]*)\]\]\]+": r"\1",  # Remove triple brackets
        r"\[\[+([^\[\]]*)\]\]+": r"\1",      # Remove double brackets
        r"\[+([^\[\]]*)\]+": r"\1",          # Remove single brackets
        r"\{\{\{+([^\{\}]*)\}\}\}+": r"\1",  # Remove triple braces
        r"\{\{+([^\{\}]*)\}\}+": r"\1",      # Remove double braces
        r"\{+([^\{\}]*)\}+": r"\1",          # Remove single braces
        r"FRND\}+\]+": "FRND",               # Clean FRND}]]
        r"Team\s*FRND\}+\]+": "Team FRND",   # Clean Team FRND}]]
        r"\}+\]+": "",                       # Clean trailing }]]
    }
    
    for pattern, replacement in fixes.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text

def fix_formatting_issues(text, target_lang):
    """Fix unnecessary spacing and cleanup across ALL languages"""
    
    # Clean leaked instructions first
    instruction_patterns = [
        r'\[translate from:.*?\]\s*',
        r'\[.*?translate.*?from.*?\]\s*',
        r'^\[.*?\]\s*',  # Any leading bracketed instructions
        r'\[INST.*?\]\s*',
        r'\[INSTRUCTION.*?\]\s*',
    ]
    
    for pattern in instruction_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    # General formatting cleanup
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

# -------------------- CHATGPT QUALITY CHECKER -------------------- #

def get_language_context_for_gpt(target_lang, mode, context_type, audience, formality_level):
    """Build detailed context instructions for ChatGPT based on Sarvam settings"""
    
    # Language-specific instructions
    lang_instructions = {
        "hi-IN": "Hindi with Roman script (Hinglish) and English code-mixing. Example: 'weekend ON ho gaya hai'",
        "ta-IN": "Tamil script with selective English words preserved. Example: 'Saturday – weekend OFFICIALLY ON!'", 
        "te-IN": "Telugu with Roman script and English code-mixing. Example: 'weekend officially ON lo undhi'",
        "ml-IN": "Malayalam script with simple English terms preserved where natural",
        "kn-IN": "Kannada script with simple English terms preserved where natural"
    }
    
    # Mode instructions
    mode_instructions = {
        "modern-colloquial": "modern, casual, conversational style",
        "formal": "formal, professional, respectful tone",
        "classic-colloquial": "literal, word-for-word accuracy prioritized",
        "code-mixed": "heavy English-local language mixing, trendy expressions"
    }
    
    # Formality mapping
    formality_descriptions = {
        1: "very casual, informal",
        2: "casual, friendly", 
        3: "neutral, balanced",
        4: "respectful, semi-formal",
        5: "very formal, professional"
    }
    
    # Build comprehensive context
    context = f"""
Language Target: {lang_instructions.get(target_lang, "the target language")}
Style Mode: {mode_instructions.get(mode, mode)}
Formality Level: {formality_descriptions.get(formality_level, "balanced")}
"""
    
    if context_type:
        context += f"Context: {CONTEXT_TYPES.get(context_type, context_type)}\n"
    
    if audience:
        context += f"Target Audience: {AUDIENCE_TYPES.get(audience, audience)}\n"
    
    return context

def chatgpt_quality_check_and_improve(original_text, sarvam_translation, target_lang, mode, context_type, audience, formality_level):
    """Use ChatGPT to quality check and improve Sarvam translation with exact same context"""
    
    if not OPENAI_API_KEY or not sarvam_translation or sarvam_translation.startswith("❌"):
        return sarvam_translation, "No ChatGPT API key or invalid Sarvam translation"
    
    # Pre-clean obvious issues in Sarvam translation before sending to ChatGPT
    cleaned_sarvam = fix_brand_name_issues(sarvam_translation, target_lang)
    cleaned_sarvam = fix_formatting_issues(cleaned_sarvam, target_lang)
    
    # Build context instructions matching Sarvam settings
    language_context = get_language_context_for_gpt(target_lang, mode, context_type, audience, formality_level)
    
    prompt = f"""TASK: Fix and improve this translation while maintaining the exact same style and context.

ORIGINAL ENGLISH:
{original_text}

TRANSLATION TO FIX:
{cleaned_sarvam}

REQUIREMENTS:
{language_context}

CRITICAL RULES:
1. Fix any bracket issues around brand names (FRND}}]], Team FRND}}]] should be FRND, Team FRND)
2. Complete any incomplete sentences
3. Fix grammar errors while keeping the same language mixing style
4. Keep exact same script (Roman/Native) and formality level
5. Preserve all emojis and formatting
6. DO NOT add explanations or comments
7. ONLY return the corrected translation text

CORRECTED TRANSLATION:"""

    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a translation editor. Return ONLY the corrected translation text with no explanations or comments."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 1000,
            "temperature": 0.1
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", 
                               headers=headers, 
                               json=payload, 
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and len(result["choices"]) > 0:
                improved_translation = result["choices"][0]["message"]["content"].strip()
                
                # Aggressive cleaning of ChatGPT meta-responses
                # Remove any explanatory text that ChatGPT might add
                meta_patterns = [
                    r'^(CORRECTED TRANSLATION|IMPROVED TRANSLATION|FIXED TRANSLATION|Translation|Final Translation|Here is the corrected translation|The corrected translation is):\s*',
                    r'The.*?translation.*?is.*?already.*?good.*?\.',
                    r'No improvements.*?needed.*?\.',
                    r'The Sarvam translation.*?is.*?already.*?\.',
                    r'This translation.*?meets.*?requirements.*?\.',
                ]
                
                for pattern in meta_patterns:
                    improved_translation = re.sub(pattern, '', improved_translation, flags=re.IGNORECASE | re.DOTALL)
                
                improved_translation = improved_translation.strip()
                
                # If ChatGPT returned explanatory text instead of translation, use cleaned Sarvam
                explanatory_phrases = [
                    "already in line with", "no improvements needed", "meets the requirements",
                    "is already good", "no changes required", "translation provided is"
                ]
                
                if any(phrase.lower() in improved_translation.lower() for phrase in explanatory_phrases):
                    improved_translation = cleaned_sarvam
                
                # Final cleanup
                improved_translation = fix_brand_name_issues(improved_translation, target_lang)
                improved_translation = fix_formatting_issues(improved_translation, target_lang)
                
                return improved_translation, None
            else:
                return cleaned_sarvam, "No response from ChatGPT"
        else:
            return cleaned_sarvam, f"ChatGPT API Error: {response.status_code}"
            
    except requests.exceptions.Timeout:
        return cleaned_sarvam, "ChatGPT timeout - using cleaned Sarvam translation"
    except requests.exceptions.ConnectionError:
        return cleaned_sarvam, "Connection error - using cleaned Sarvam translation"
    except Exception as e:
        return cleaned_sarvam, f"ChatGPT error: {str(e)}"

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
        # 1. Clean leaked instructions - more comprehensive patterns
        result = re.sub(r'\[INSTRUCTION:.*?\]\s*', '', result, flags=re.IGNORECASE)
        result = re.sub(r'\[INST:.*?\]\s*', '', result, flags=re.IGNORECASE)
        result = re.sub(r'\[Translate completely including:.*?\]\s*', '', result, flags=re.IGNORECASE)
        result = re.sub(r'\[translate from:.*?\]\s*', '', result, flags=re.IGNORECASE)  # New pattern
        result = re.sub(r'\[.*?translate.*?from.*?\]\s*', '', result, flags=re.IGNORECASE)  # Broader pattern
        result = re.sub(r'^\[.*?\]\s*', '', result, flags=re.MULTILINE)  # Any leading bracketed text
        
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
st.title("🎯 FRND Enhanced Translator with AI Quality Check")
st.markdown("*Sarvam translation enhanced by ChatGPT quality checking*")

# Quality improvements info
with st.expander("🔧 Enhanced Quality Process"):
    st.markdown("""
    **Translation Process:**
    1. 🎯 **Sarvam Translation**: Initial translation with optimized settings
    2. 🤖 **ChatGPT Quality Check**: Reviews and refines the Sarvam translation using identical context settings
    3. ✨ **Final Result**: Best of both - Sarvam's contextual accuracy + ChatGPT's quality refinement
    
    **Universal Improvements:**
    - 🎯 **Complete Translations**: Ensures all parts are translated
    - 🔧 **Brand Protection**: Preserves FRND brand formatting
    - 📝 **Quality Assurance**: ChatGPT reviews for grammar and naturalness
    - 🎨 **Context Consistency**: Same language patterns maintained throughout
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
    
    # Enable/disable ChatGPT quality checking
    enable_chatgpt_qa = st.checkbox("🤖 Enable ChatGPT Quality Enhancement", 
                                   value=True,
                                   help="Use ChatGPT to review and improve Sarvam translation")
    
    col_gender, col_mode = st.columns(2)
    with col_gender:
        gender = st.selectbox("Gender:", ["Male", "Female"])
    with col_mode:
        mode_ui = st.selectbox("Style:", list(MODE_OPTIONS.keys()), index=3)  # Default to Blended

# Translate button
if st.button("🔄 Translate with AI Quality Enhancement", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter text to translate.")
    else:
        with st.spinner("Step 1/2: Getting Sarvam translation..."):
            src = LANG_MAP[source_ui]
            tgt = LANG_MAP[target_ui]
            selected_mode = MODE_OPTIONS[mode_ui]
            
            # Get Sarvam translation
            sarvam_result = translate_text(
                text.strip(), src, tgt, gender, selected_mode,
                context_type, audience, formality_level
            )
            
            # Calculate initial confidence
            initial_quality_flags, initial_confidence = analyze_translation_quality(
                text.strip(), sarvam_result, src, tgt
            )
        
        # ChatGPT Quality Enhancement
        final_translation = sarvam_result
        gpt_error = None
        gpt_status = "Disabled"
        
        if enable_chatgpt_qa and not sarvam_result.startswith("❌"):
            with st.spinner("Step 2/2: ChatGPT quality enhancement..."):
                final_translation, gpt_error = chatgpt_quality_check_and_improve(
                    text.strip(), sarvam_result, tgt, selected_mode, 
                    context_type, audience, formality_level
                )
                gpt_status = "Enhanced" if not gpt_error else f"Error: {gpt_error}"
        
        # Calculate final confidence
        final_quality_flags, final_confidence = analyze_translation_quality(
            text.strip(), final_translation, src, tgt
        )
        
        # Store results
        st.session_state.sarvam_translation = sarvam_result
        st.session_state.final_translation = final_translation
        st.session_state.gpt_status = gpt_status
        st.session_state.gpt_error = gpt_error
        st.session_state.original_text = text
        st.session_state.source_lang = source_ui
        st.session_state.target_lang_ui = target_ui
        st.session_state.initial_confidence = initial_confidence
        st.session_state.final_confidence = final_confidence
        st.session_state.initial_quality_flags = initial_quality_flags
        st.session_state.final_quality_flags = final_quality_flags

# Display results
if 'final_translation' in st.session_state:
    st.divider()
    st.subheader("📋 Translation Results")
    
    # Show process steps
    col_process1, col_process2, col_process3 = st.columns(3)
    with col_process1:
        st.info("**Step 1**: Sarvam Translation ✅")
    with col_process2:
        gpt_status = st.session_state.get('gpt_status', 'Disabled')
        if gpt_status == "Enhanced":
            st.success("**Step 2**: ChatGPT Enhanced ✅")
        elif gpt_status == "Disabled":
            st.warning("**Step 2**: ChatGPT Disabled")
        else:
            st.error(f"**Step 2**: {gpt_status}")
    with col_process3:
        final_conf = st.session_state.get('final_confidence', 0)
        if final_conf >= 0.8:
            st.success("**Quality**: Excellent ✅")
        elif final_conf >= 0.7:
            st.info("**Quality**: Good 📊")
        else:
            st.error("**Quality**: Needs Review ⚠️")
    
    # Show translations
    if st.session_state.get('gpt_status') == "Enhanced":
        # Show before/after comparison
        col_before, col_after = st.columns(2)
        
        with col_before:
            st.markdown("### 🎯 Initial Sarvam Translation")
            st.text_area("Sarvam Output:", value=st.session_state.sarvam_translation, height=120, key="sarvam_output")
            initial_conf = st.session_state.get('initial_confidence', 0)
            if initial_conf >= 0.8:
                st.success(f"Initial Confidence: {initial_conf:.1%}")
            elif initial_conf >= 0.7:
                st.info(f"Initial Confidence: {initial_conf:.1%}")
            else:
                st.error(f"Initial Confidence: {initial_conf:.1%}")
            
        with col_after:
            st.markdown("### ✨ ChatGPT Enhanced Translation")
            st.text_area("Final Output:", value=st.session_state.final_translation, height=120, key="final_output")
            final_conf = st.session_state.get('final_confidence', 0)
            if final_conf >= 0.8:
                st.success(f"Final Confidence: {final_conf:.1%}")
            elif final_conf >= 0.7:
                st.info(f"Final Confidence: {final_conf:.1%}")
            else:
                st.error(f"Final Confidence: {final_conf:.1%}")
    else:
        # Single translation display
        st.markdown("### 🎯 Final Translation")
        st.text_area("Translation Result:", value=st.session_state.final_translation, height=150, key="translation_output")
        
        # Show any ChatGPT errors
        if st.session_state.get('gpt_error'):
            st.warning(f"ChatGPT Quality Check: {st.session_state.gpt_error}")
    
    # Overall Quality Analysis
    if not st.session_state.final_translation.startswith("❌"):
        st.subheader("📊 Overall Quality Assessment")
        
        final_conf = st.session_state.get('final_confidence', 0)
        initial_conf = st.session_state.get('initial_confidence', 0)
        
        # Show confidence improvement
        col_conf1, col_conf2, col_conf3 = st.columns(3)
        with col_conf1:
            st.metric("Initial Confidence", f"{initial_conf:.1%}")
        with col_conf2:
            st.metric("Final Confidence", f"{final_conf:.1%}", f"{final_conf - initial_conf:.1%}")
        with col_conf3:
            improvement = "Enhanced" if final_conf > initial_conf else "Maintained" if final_conf == initial_conf else "Degraded"
            improvement_color = "normal" if improvement == "Maintained" else "inverse" if improvement == "Enhanced" else "off"
            st.metric("Quality Status", improvement, delta_color=improvement_color)
        
        # Show quality flags if any
        final_quality_flags = st.session_state.get('final_quality_flags', [])
        if final_quality_flags:
            st.subheader("🔍 Quality Issues Detected")
            for flag in final_quality_flags:
                st.info(flag)
        else:
            if final_conf >= 0.7:
                st.success("✅ Translation meets enhanced quality standards")
            else:
                st.warning("⚠️ Translation may need manual review")
    
    # Action buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    with col_btn1:
        st.download_button("📥 Download Translation", st.session_state.final_translation, 
            file_name=f"translation_{st.session_state.target_lang_ui.lower()}.txt")
    with col_btn2:
        if st.button("🔄 Retranslate"):
            st.rerun()
    with col_btn3:
        if st.button("⭐ Mark as Approved"):
            st.success("Translation approved!")
    
    # Additional insights
    if st.session_state.get('gpt_status') == "Enhanced":
        with st.expander("🔍 Translation Process Details"):
            st.markdown("""
            **Process Completed:**
            1. ✅ Sarvam provided initial translation with your exact context settings
            2. ✅ ChatGPT reviewed the translation for quality issues
            3. ✅ ChatGPT applied improvements while maintaining the same style and context
            4. ✅ Final translation combines Sarvam's contextual accuracy with ChatGPT's quality refinement
            
            **Benefits:**
            - Same language patterns and formality as specified
            - Enhanced grammar and naturalness
            - Consistent brand name handling
            - Improved overall readability
            """)

# Help section
with st.expander("ℹ️ AI Quality Enhancement Guide"):
    st.markdown("""
    **How AI Quality Enhancement Works:**
    
    **Step 1: Sarvam Translation**
    - Uses your exact language, context, and formality settings
    - Applies brand protection and completeness optimizations
    - Generates contextually accurate translation
    
    **Step 2: ChatGPT Quality Review** (if enabled)
    - Reviews Sarvam translation for quality issues
    - Maintains the exact same context settings and language patterns
    - Only improves grammar, naturalness, and completeness
    - Preserves the original translation approach and style
    
    **Final Result:**
    - Best of both: Sarvam's contextual expertise + ChatGPT's quality refinement
    - Single high-quality translation instead of competing versions
    - Confidence score reflects overall translation quality
    
    **When to Use:**
    - ✅ **Enable**: For important content requiring highest quality
    - ⚠️ **Consider**: May slightly increase translation time
    - 💡 **Benefit**: Significantly improved grammar and naturalness while maintaining context
    """)

st.markdown("---")
st.markdown("*FRND Enhanced Translator • AI-Powered Quality Assurance*")
