import os
import streamlit as st
from dotenv import load_dotenv
import requests
import re
import emoji
import csv
import io
from datetime import datetime

# Import the combined translation enhancements
from translation_enhancements import (
    enhanced_preprocess_input_for_completeness,
    enhanced_postprocess_translation_output, 
    get_enhanced_chatgpt_prompt_with_training,
    analyze_enhanced_translation_quality,
    clean_instruction_leaks_from_result,
    get_enhancement_info
)

# Load environment variables
load_dotenv()
API_KEY = os.getenv("SARVAM_API_KEY", st.secrets.get("SARVAM_API_KEY", ""))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))

st.set_page_config(page_title="FRND Quality Translator", layout="wide")

# -------------------- CSV LOGGING FUNCTIONS -------------------- #

def get_csv_filename():
    """Get the CSV filename for logging translations"""
    return "translation_logs.csv"

def initialize_csv_file():
    """Initialize CSV file with headers if it doesn't exist"""
    filename = get_csv_filename()
    
    if not os.path.exists(filename):
        headers = ["Input Language", "Output Language", "Input Text", "Output Text", "Timestamp"]
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)
        return True
    return False

def log_translation_to_csv(input_lang, output_lang, input_text, output_text):
    """Log translation to CSV file with timestamp"""
    try:
        filename = get_csv_filename()
        initialize_csv_file()
        
        # Preserve line breaks in CSV by replacing newlines with a safe marker
        input_text_safe = input_text.replace('\n', ' | ').replace('\r', '') if input_text else ""
        output_text_safe = output_text.replace('\n', ' | ').replace('\r', '') if output_text else ""
        
        # Add timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Prepare new row with timestamp
        new_row = [input_lang, output_lang, input_text_safe, output_text_safe, timestamp]
        
        # Append to CSV
        with open(filename, 'a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)
        
        return True, None
        
    except Exception as e:
        return False, str(e)

def get_monthly_csv_data():
    """Get translations from current month only"""
    try:
        filename = get_csv_filename()
        if not os.path.exists(filename):
            return None, "No translation logs found"
        
        # Get current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        monthly_data = []
        
        with open(filename, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            headers = next(reader)  # Get header row
            
            # Ensure headers include timestamp
            if len(headers) < 5:
                headers.append("Timestamp")
            
            monthly_data.append(headers)
            
            for row in reader:
                if len(row) >= 4:  # Ensure row has minimum required data
                    # Check if timestamp exists and is from current month
                    if len(row) >= 5 and row[4]:
                        try:
                            # Parse existing timestamp
                            timestamp = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S")
                            if timestamp.month == current_month and timestamp.year == current_year:
                                monthly_data.append(row)
                        except:
                            # If timestamp parsing fails, skip this row
                            continue
                    else:
                        # For rows without timestamp, add current timestamp and include
                        # (this handles old data without timestamps)
                        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if len(row) == 4:
                            row.append(current_timestamp)
                            monthly_data.append(row)
        
        if len(monthly_data) <= 1:  # Only headers
            return None, f"No translations found for {datetime.now().strftime('%B %Y')}"
        
        return monthly_data, None
        
    except Exception as e:
        return None, f"Error reading CSV: {str(e)}"

# -------------------- CONFIG -------------------- #

LANG_MAP = {
    "Hindi": "hi-IN", "Kannada": "kn-IN", "Telugu": "te-IN", "Tamil": "ta-IN", "Malayalam": "ml-IN",
    "Bengali": "bn-IN", "Gujarati": "gu-IN", "Punjabi": "pa-IN", "Marathi": "mr-IN", "Odia": "or-IN",
    "English": "en-IN"
}

# Language-specific script and code-mixing preferences
LANGUAGE_PATTERNS = {
    "hi-IN": {"script": "roman", "mode": "code-mixed"},
    "te-IN": {"script": "roman", "mode": "code-mixed"},
    "ta-IN": {"script": "mixed", "mode": "modern-colloquial"},
    "ml-IN": {"script": "fully-native", "mode": "formal"},
    "kn-IN": {"script": "fully-native", "mode": "formal"},
    "or-IN": {"script": "mixed", "mode": "modern-colloquial"}
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
        return {"script": "roman", "mode": "modern-colloquial"}

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
            r'(?<=[.।!?❌])\s+(?=[🚫🚨🔗📱📲✅💙—•])',
            r'(?<=[🚫])\s+(?=[A-Z])', r'(?<=[💙])\s+(?=[—])',
            r'(?<=hai\.)\s+(?=[🚨])', r'(?<=hain\.)\s+(?=[A-Z🚨])',
            r'(?<=[📱📲])\s+(?=[✅])', r'(?<=hai\.)\s+(?=[A-Z])',
        ]
        
        for pattern in sentence_patterns:
            potential_lines = re.split(pattern, translated_text.strip())
            if len(potential_lines) >= 2:
                return "\n".join(potential_lines)
        
        # Fallback: Split by emojis
        emoji_break_pattern = r'(?<=[.।!?])\s+(?=[🚫🚨✅💙—])'
        lines = re.split(emoji_break_pattern, translated_text.strip())
        if len(lines) > 1:
            return "\n".join(lines)
    
    return translated_text

def fix_brand_name_issues(text, target_lang):
    """Fix brand name formatting issues"""
    fixes = {
        r"\[\[\[+([^\[\]]*)\]\]\]+": r"\1", r"\[\[+([^\[\]]*)\]\]+": r"\1", r"\[+([^\[\]]*)\]+": r"\1",
        r"\{\{\{+([^\{\}]*)\}\}\}+": r"\1", r"\{\{+([^\{\}]*)\}\}+": r"\1", r"\{+([^\{\}]*)\}+": r"\1",
        r"FRND\}+\]+": "FRND", r"Team\s*FRND\}+\]+": "Team FRND", r"\}+\]+": "",
        r"^\]+,?\s*": "", r"\]+,\s*": "", r"\]+\s*": "", r"^\s*,\s*": "",
    }
    
    for pattern, replacement in fixes.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE | re.MULTILINE)
    
    return text

def fix_formatting_issues(text, target_lang):
    """Fix unnecessary spacing and cleanup"""
    instruction_patterns = [
        r'\[translate from:.*?\]\s*', r'\[.*?translate.*?from.*?\]\s*', r'^\[.*?\]\s*',
        r'\[INST.*?\]\s*', r'\[INSTRUCTION.*?\]\s*',
    ]
    
    for pattern in instruction_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.MULTILINE)
    
    # Clean remaining bracket artifacts
    bracket_artifacts = [r'^\]+,?\s*', r'\]+,\s*', r'\]+\s*', r'^\s*,\s*', r',\s*,\s*']
    
    for pattern in bracket_artifacts:
        text = re.sub(pattern, '', text, flags=re.MULTILINE)
    
    # General formatting cleanup
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    return text

def enhance_catchy_phrases(text, target_lang):
    """Improve translation of catchy/marketing phrases"""
    catchy_phrases = {
        "What is the scene": {
            "hi-IN": "Scene kya hai", "ta-IN": "Scene என்னங்க", "te-IN": "Scene entante",
            "ml-IN": "എന്താണ് scene", "kn-IN": "Scene ಏನು"
        },
        "Take the first step": {
            "hi-IN": "Pehla step lo", "ta-IN": "First step எடுங்க", "te-IN": "Modati step teeskondi",
            "ml-IN": "ആദ്യ step എടുക്കൂ", "kn-IN": "ಮೊದಲ step ತೆಗೆದುಕೊಳ್ಳಿ"
        },
        "lighthearted call": {
            "hi-IN": "casual call", "ta-IN": "lighthearted-ஆ call", "te-IN": "casual ga call",
            "ml-IN": "സുഖമായി call", "kn-IN": "ಸುಲಭವಾಗಿ call"
        }
    }
    
    for phrase, translations in catchy_phrases.items():
        if phrase.lower() in text.lower() and target_lang in translations:
            text = re.sub(re.escape(phrase), translations[target_lang], text, flags=re.IGNORECASE)
    
    return text

# -------------------- MAIN TRANSLATION FUNCTION -------------------- #

def translate_text(text, source_lang, target_lang, gender, mode, context_type="", audience="", formality_level=3):
    """Enhanced translate function using the combined training patterns"""
    
    # Get language-specific settings
    lang_pattern = get_language_specific_settings(target_lang)
    
    # Override mode based on language pattern
    if mode == "modern-colloquial":
        mode = lang_pattern["mode"]
    
    # ENHANCED INPUT PREPROCESSING WITH ALL 3 TRAINING LAYERS
    enhanced_text = enhanced_preprocess_input_for_completeness(text, target_lang)
    
    # Apply basic catchy phrase enhancements
    enhanced_text = enhance_catchy_phrases(enhanced_text, target_lang)
    
    # Prepare for API
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
        "API-Subscription-key": API_KEY
    }

    response = requests.post("https://api.sarvam.ai/translate", json=payload, headers=headers)

    if response.status_code == 200:
        result_raw = response.json().get("translated_text", "")
        result = untag_preserved_words(result_raw)
        result = restore_multiline_output(result, text)
        
        # Clean leaked instructions using enhanced function
        result = clean_instruction_leaks_from_result(result)
        
        # Apply basic fixes
        result = fix_brand_name_issues(result, target_lang)
        result = fix_formatting_issues(result, target_lang)
        
        # ENHANCED OUTPUT POST-PROCESSING WITH ALL 3 TRAINING LAYERS
        result = enhanced_postprocess_translation_output(result, target_lang)
        
        return result
    else:
        return f"❌ Error: {response.status_code} - {response.text}"

# -------------------- ENHANCED CHATGPT QUALITY CHECKER -------------------- #

def chatgpt_quality_check_and_improve(original_text, sarvam_translation, target_lang, mode, context_type, audience, formality_level):
    """Enhanced ChatGPT quality checker using combined training patterns"""
    
    if not OPENAI_API_KEY or not sarvam_translation or sarvam_translation.startswith("❌"):
        return sarvam_translation, "No ChatGPT API key or invalid Sarvam translation"
    
    # Pre-clean obvious issues
    cleaned_sarvam = fix_brand_name_issues(sarvam_translation, target_lang)
    cleaned_sarvam = fix_formatting_issues(cleaned_sarvam, target_lang)
    
    # Get enhanced prompt with all training examples
    prompt = get_enhanced_chatgpt_prompt_with_training(
        original_text, cleaned_sarvam, target_lang, mode, context_type, audience, formality_level
    )

    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are a translation editor with access to comprehensive training examples. Follow ALL training patterns exactly. Return ONLY the corrected translation text with no explanations or comments."},
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
                
                # Final cleanup using enhanced functions
                improved_translation = clean_instruction_leaks_from_result(improved_translation)
                improved_translation = fix_brand_name_issues(improved_translation, target_lang)
                improved_translation = fix_formatting_issues(improved_translation, target_lang)
                improved_translation = enhanced_postprocess_translation_output(improved_translation, target_lang)
                
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

def check_cultural_sensitivity(text, target_lang):
    """Check for potentially sensitive content"""
    warnings = []
    text_lower = text.lower()
    
    if any(word in text_lower for word in ["pork", "beef", "alcohol"]):
        warnings.append("🔍 Contains potentially sensitive content - please review cultural appropriateness")
    
    if any(word in text_lower for word in ["christmas", "diwali", "eid", "holi", "rakhi", "raksha bandhan"]):
        warnings.append("📅 Contains festival references - ensure timing is appropriate")
    
    if any(word in text_lower for word in ["loan", "debt", "payment", "money"]):
        warnings.append("💰 Contains financial terms - ensure compliance with regulations")
    
    return warnings

# -------------------- STREAMLIT UI -------------------- #

st.title("🎯 FRND Enhanced Translator with AI Quality Check")

# Show enhancement info
enhancement_info = get_enhancement_info()
st.markdown(f"*Enhanced with {enhancement_info['version']} - {', '.join(enhancement_info['training_layers'])} training*")

# Quality improvements info
with st.expander("🔧 Enhanced Quality Process"):
    st.markdown(f"""
    **Translation Process with {enhancement_info['version']} Enhancements:**
    1. 🎯 **Sarvam Translation**: Initial translation with {len(enhancement_info['training_layers'])} layers of training patterns
    2. 🤖 **ChatGPT Quality Check**: Reviews using comprehensive training examples
    3. ✨ **Final Result**: Best quality translation with all patterns applied
    
    **Training Layers:**
    - 🎤 **Layer 1**: Meeting/Live session patterns
    - 📱 **Layer 2**: WhatsApp Channel/Privacy patterns  
    - 🎊 **Layer 3**: Festival/Holiday patterns (Rakhi focus)
    
    **Supported Languages:** {', '.join(enhancement_info['supported_languages'])}
    
    **Universal Improvements:**
    - 🎯 **Complete Translations**: All parts translated using training patterns
    - 🔧 **Brand Protection**: Preserves FRND brand formatting
    - 📝 **Quality Assurance**: ChatGPT reviews using comprehensive training examples
    - 🎨 **Context Consistency**: Festival, WhatsApp, and meeting contexts handled appropriately
    - 🎊 **Festival Support**: Optimized for Rakhi, holidays, and cultural celebrations
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
                                   help="Use ChatGPT to review and improve Sarvam translation with training examples")
    
    col_gender, col_mode = st.columns(2)
    with col_gender:
        gender = st.selectbox("Gender:", ["Male", "Female"])
    with col_mode:
        mode_ui = st.selectbox("Style:", list(MODE_OPTIONS.keys()), index=3)

# Translate button
if st.button("🔄 Translate with Enhanced AI Quality", type="primary", use_container_width=True):
    if not text.strip():
        st.warning("Please enter text to translate.")
    else:
        with st.spinner("Step 1/2: Getting enhanced Sarvam translation..."):
            src = LANG_MAP[source_ui]
            tgt = LANG_MAP[target_ui]
            selected_mode = MODE_OPTIONS[mode_ui]
            
            # Get Sarvam translation with enhanced training
            sarvam_result = translate_text(
                text.strip(), src, tgt, gender, selected_mode,
                context_type, audience, formality_level
            )
            
            # Calculate initial confidence using enhanced analysis
            initial_quality_flags, initial_confidence = analyze_enhanced_translation_quality(
                text.strip(), sarvam_result, src, tgt
            )
        
        # ChatGPT Quality Enhancement
        final_translation = sarvam_result
        gpt_error = None
        gpt_status = "Disabled"
        
        if enable_chatgpt_qa and not sarvam_result.startswith("❌"):
            with st.spinner("Step 2/2: ChatGPT quality enhancement with training examples..."):
                final_translation, gpt_error = chatgpt_quality_check_and_improve(
                    text.strip(), sarvam_result, tgt, selected_mode, 
                    context_type, audience, formality_level
                )
                gpt_status = "Enhanced" if not gpt_error else f"Error: {gpt_error}"
        
        # Calculate final confidence using enhanced analysis
        final_quality_flags, final_confidence = analyze_enhanced_translation_quality(
            text.strip(), final_translation, src, tgt
        )
        
        # Log translation to CSV
        if not final_translation.startswith("❌"):
            log_success, log_error = log_translation_to_csv(
                source_ui, target_ui, text.strip(), final_translation
            )
            if not log_success:
                st.warning(f"Failed to log to CSV: {log_error}")
        
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
        st.info("**Step 1**: Enhanced Sarvam ✅")
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
            st.markdown("### 🎯 Enhanced Sarvam Translation")
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
    
    # Enhanced Quality Analysis
    if not st.session_state.final_translation.startswith("❌"):
        st.subheader("📊 Enhanced Quality Assessment")
        
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
        
        # Show enhanced quality flags if any
        final_quality_flags = st.session_state.get('final_quality_flags', [])
        if final_quality_flags:
            st.subheader("🔍 Quality Issues Detected")
            for flag in final_quality_flags:
                st.info(flag)
        else:
            if final_conf >= 0.7:
                st.success("✅ Translation meets enhanced quality standards with training patterns")
            else:
                st.warning("⚠️ Translation may need manual review")
    
    # Action buttons with monthly CSV download
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    with col_btn1:
        st.download_button("📥 Download Translation", st.session_state.final_translation, 
            file_name=f"translation_{st.session_state.target_lang_ui.lower()}.txt")
    with col_btn2:
        # Download ALL CSV logs
        csv_file = get_csv_filename()
        if os.path.exists(csv_file):
            with open(csv_file, "rb") as file:
                st.download_button("📊 All Logs (Excel)", file.read(), 
                    file_name="translation_logs_all.csv", mime="text/csv")
    with col_btn3:
        # Download THIS MONTH's CSV logs only
        monthly_data, error = get_monthly_csv_data()
        if monthly_data:
            # Convert to CSV string
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerows(monthly_data)
            csv_string = output.getvalue()
            
            current_month_name = datetime.now().strftime("%B_%Y")
            st.download_button(
                f"📅 {datetime.now().strftime('%B')} Logs", 
                csv_string, 
                file_name=f"translations_{current_month_name}.csv", 
                mime="text/csv"
            )
        else:
            st.download_button(
                f"📅 {datetime.now().strftime('%B')} Logs", 
                "No data for this month", 
                file_name=f"translations_{datetime.now().strftime('%B_%Y')}.csv", 
                mime="text/csv",
                disabled=True
            )
    with col_btn4:
        if st.button("🔄 Retranslate"):
            st.rerun()
    
    # Additional insights
    if st.session_state.get('gpt_status') == "Enhanced":
        with st.expander("🔍 Enhanced Translation Process Details"):
            st.markdown(f"""
            **Process Completed with Training Enhancement {enhancement_info['version']}:**
            1. ✅ Sarvam provided initial translation with {len(enhancement_info['training_layers'])} training layers applied
            2. ✅ ChatGPT reviewed using comprehensive training examples from all contexts
            3. ✅ ChatGPT applied improvements while maintaining exact style and context
            4. ✅ Final translation optimized for: {', '.join(enhancement_info['training_layers'])}
            
            **Training Benefits:**
            - Festival/Holiday context optimization (Rakhi, celebrations)
            - WhatsApp Channel promotion accuracy
            - Meeting/Live session natural flow
            - Enhanced cultural sensitivity and brand protection
            - Improved grammar and naturalness across all contexts
            
            **Pattern Coverage:**
            - Total Training Patterns: {enhancement_info['total_patterns']}
            - Total Quality Fixes: {enhancement_info['total_fixes']}
            - Last Updated: {enhancement_info['last_updated']}
            """)

# Enhanced Help section
with st.expander("ℹ️ Enhanced AI Quality Guide"):
    st.markdown(f"""
    **How Enhanced AI Quality Works (Version {enhancement_info['version']}):**
    
    **Step 1: Enhanced Sarvam Translation**
    - Uses your exact language, context, and formality settings
    - Applies {len(enhancement_info['training_layers'])} layers of training patterns:
      * 🎤 Meeting/Live session patterns
      * 📱 WhatsApp Channel/Privacy patterns
      * 🎊 Festival/Holiday patterns (Rakhi focus)
    - Generates contextually accurate translation with training optimization
    
    **Step 2: ChatGPT Quality Review with Training Examples** (if enabled)
    - Reviews Sarvam translation using comprehensive training examples
    - Maintains exact same context settings and language patterns
    - Applies improvements based on proven quality patterns
    - Preserves cultural context and brand formatting
    
    **Final Result:**
    - Best quality translation with all training patterns applied
    - Enhanced confidence scoring with training pattern compliance
    - Context-aware quality assessment (Festival, WhatsApp, Meeting contexts)
    
    **When to Use:**
    - ✅ **Enable**: For all important content requiring highest quality
    - 🎊 **Festivals**: Optimized for Rakhi, holidays, cultural celebrations
    - 📱 **WhatsApp**: Perfect for channel promotions and privacy messaging
    - 🎤 **Meetings**: Ideal for live sessions and professional communication
    - 💡 **Benefit**: Training-enhanced accuracy with cultural sensitivity
    
    **Training Data Sources:**
    - Real FRND translation examples
    - Festival and cultural content optimization
    - WhatsApp channel promotion patterns
    - Meeting and live session flows
    """)

# Training info section
with st.expander("📚 Training Enhancement Details"):
    st.markdown(f"""
    **Current Training Version: {enhancement_info['version']}**
    
    **Training Layers:**
    1. **Layer 1 - Meeting/Live Sessions**: Natural conversation flow for live interactions
    2. **Layer 2 - WhatsApp/Privacy**: Channel promotions and privacy-focused messaging  
    3. **Layer 3 - Festival/Holiday**: Cultural celebrations, especially Rakhi and holidays
    
    **Language Support:**
    - Hindi (Hinglish mixing)
    - Tamil (Tamil-English mixing)
    - Telugu (Telugu-English mixing)
    - Malayalam (Native-focused)
    - Kannada (Native-focused)
    - Odia (Native with English terms)
    
    **Quality Improvements:**
    - Context-aware pattern application
    - Cultural sensitivity optimization
    - Brand name protection (FRND)
    - Emoji and formatting preservation
    - Training pattern compliance scoring
    
    **Daily Updates:**
    - Translation patterns file can be updated daily
    - App.py remains stable and unchanged
    - New training data seamlessly integrated
    """)

# CSV Download Info section
with st.expander("📊 CSV Download Options"):
    st.markdown(f"""
    **Translation Logging:**
    - All translations are automatically logged with timestamps
    - CSV format perfect for Excel analysis
    - Tracks: Input/Output languages, texts, and timestamps
    
    **Download Options:**
    - 📊 **All Logs**: Complete translation history (all months)
    - 📅 **{datetime.now().strftime('%B')} Logs**: Current month translations only
    - 📥 **Single Translation**: Individual text file download
    
    **Monthly Filtering:**
    - Automatically filters by current calendar month
    - Perfect for monthly reports and analysis
    - Excel-compatible format with proper headers
    
    **Use Cases:**
    - Monthly performance tracking
    - Content analysis and review
    - Quality improvement insights
    - Team collaboration and sharing
    """)

st.markdown("---")

# Show current enhancement status
col_status1, col_status2, col_status3 = st.columns(3)
with col_status1:
    st.metric("Enhancement Version", enhancement_info['version'])
with col_status2:
    st.metric("Training Layers", len(enhancement_info['training_layers']))
with col_status3:
    st.metric("Supported Languages", len(enhancement_info['supported_languages']))

st.markdown(f"*FRND Enhanced Translator • AI-Powered Quality Assurance • Training v{enhancement_info['version']} • Monthly CSV Logging*")
