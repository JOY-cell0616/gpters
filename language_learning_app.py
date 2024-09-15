import streamlit as st
from anthropic import Anthropic
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize Claude API client
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def claude_query(prompt):
    try:
        message = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=2000,
            messages=[
                {"role": "user", "content": prompt + "\n\n모든 응답은 한국어로 제공해 주세요."}
            ]
        )
        return message.content[0].text
    except Exception as e:
        st.error(f"Claude API 오류: {str(e)}")
        return None

def generate_lesson(language, difficulty, custom_text=None):
    st.subheader(f"{language} - {difficulty} 레벨 학습")
    
    texts = {
        "영어": {
            "초급": "The quick brown fox jumps over the lazy dog.",
            "중급": "Despite the heavy rain, she decided to go for a walk in the park.",
            "고급": "The intricate balance of ecosystems demonstrates the interdependence of all living organisms."
        },
        "스페인어": {
            "초급": "El rápido zorro marrón salta sobre el perro perezoso.",
            "중급": "A pesar de la fuerte lluvia, ella decidió dar un paseo por el parque.",
            "고급": "El equilibrio intrincado de los ecosistemas demuestra la interdependencia de todos los organismos vivos."
        },
        "일본어": {
            "초급": "速い茶色のキツネは怠けている犬を飛び越えます。",
            "중급": "激しい雨にもかかわらず、彼女は公園を散歩することにしました。",
            "고급": "生態系の複雑なバランスは、全ての生物の相互依存性を示しています。"
        }
    }
    
    original_text = custom_text or texts[language][difficulty]
    st.write("원문:", original_text)
    
    # 번역
    translation_prompt = f"다음 {language} 텍스트를 한국어로 번역해주세요: '{original_text}'. 번역 결과만 제공해 주세요."
    translated = claude_query(translation_prompt)
    if translated:
        st.write("번역:", translated)
    
    # 어휘 학습
    vocabulary_prompt = f"이 {language} 문장에서 {difficulty} 수준의 학습자에게 적합한 5개의 주요 어휘를 선택하고 설명해주세요: '{original_text}'"
    vocabulary_explanation = claude_query(vocabulary_prompt)
    if vocabulary_explanation:
        st.subheader("주요 어휘")
        st.write(vocabulary_explanation)
    
    # 문법 설명
    grammar_prompt = f"이 {language} 문장에서 {difficulty} 수준에 맞는 주요 문법 포인트를 설명해주세요: '{original_text}'"
    grammar_explanation = claude_query(grammar_prompt)
    if grammar_explanation:
        st.subheader("문법 포인트")
        st.write(grammar_explanation)
    
    # 발음 가이드
    pronunciation_prompt = f"이 {language} 문장의 발음 가이드를 제공해주세요: '{original_text}'"
    pronunciation_guide = claude_query(pronunciation_prompt)
    if pronunciation_guide:
        st.subheader("발음 가이드")
        st.write(pronunciation_guide)
    
    # 문화적 참고 사항
    culture_prompt = f"이 {language} 문장과 관련된 문화적 맥락이나 흥미로운 사실을 제공해주세요: '{original_text}'"
    cultural_notes = claude_query(culture_prompt)
    if cultural_notes:
        st.subheader("문화적 참고 사항")
        st.write(cultural_notes)
    
    # 퀴즈
    st.subheader("퀴즈")
    questions = [
        "이 문장에 나오는 동물은 무엇인가요?",
        "문장에서 형용사를 찾아보세요.",
        "이 문장의 주요 주제는 무엇인가요?"
    ]
    
    # 세션 상태에 답변 저장
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = [''] * len(questions)
    
    for i, question in enumerate(questions):
        st.write(f"질문 {i+1}: {question}")
        st.session_state.quiz_answers[i] = st.text_input(f"답변 {i+1}", value=st.session_state.quiz_answers[i], key=f"answer_{i}")

    if st.button("답변 제출"):
        all_answers_text = "\n".join([f"질문 {i+1}: {q}\n답변: {a}" for i, (q, a) in enumerate(zip(questions, st.session_state.quiz_answers))])
        evaluation_prompt = f"다음 문장에 대한 퀴즈 답변을 평가해주세요: '{original_text}'\n\n{all_answers_text}"
        evaluation = claude_query(evaluation_prompt)
        st.write("평가 결과:", evaluation)

    # 세션 상태 초기화 버튼
    if st.button("새로운 학습 시작"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.experimental_rerun()

def main():
    st.title("언어 학습 보조 도구")
    language = st.selectbox("학습할 언어를 선택하세요:", ["영어", "스페인어", "일본어"])
    difficulty = st.radio("난이도를 선택하세요:", ["초급", "중급", "고급"])
    custom_text = st.text_input("직접 문장을 입력하세요 (선택사항):")
    if st.button("학습 시작"):
        generate_lesson(language, difficulty, custom_text)

if __name__ == "__main__":
    main()