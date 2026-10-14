import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from database import run_query
from ai_queries import generate_sql, explain_results
BASE = Path(__file__).resolve().parent
load_dotenv(BASE / '.env')
st.set_page_config(page_title='Synthetic Clinic Assistant',page_icon='🩺',layout='wide')
st.title('Synthetic Clinic Data Assistant')
st.caption('Fictional data only • Database reference date: October 13, 2026 • Not clinical advice')
if not (BASE / 'clinic.db').exists():
    st.error('Database missing. Run python seed_database.py first.')
    st.stop()
with st.sidebar:
    st.header('Project information')
    st.write('100 fictional patients, 8 providers, and 500 visits.')
    st.write('Flow: question → GPT → SQL → SQLite → GPT → answer')
    st.write('Suggested questions:')
    for q in ['How many patients have diabetes?', 'Which provider had the most visits last month?',
              'What is the average age of patients with asthma?', 'Which patients have never had a visit?',
              'What are the most common active prescriptions among patients with hypertension?']:
        st.write('• '+q)
    st.warning('Each submitted question uses paid API calls. Keep your key private.')
key=os.getenv('OPENAI_API_KEY','')
model=os.getenv('OPENAI_MODEL','gpt-4o-mini')
with st.form('question_form'):
    question=st.text_area('Ask a question about the clinic database',max_chars=1500)
    submitted=st.form_submit_button('Ask the database')
if submitted:
    if not question.strip():
        st.warning('Enter a question first.')
    elif not key:
        st.error('Add your OpenAI API key to .env and restart the app.')
    else:
        generated=None
        try:
            with st.spinner('Generating and running a read-only query…'):
                generated=generate_sql(question,key,model)
                if generated['sql'] is None:
                    st.info(generated['explanation'])
                else:
                    result=run_query(generated['sql'])
                    answer=explain_results(question,generated['sql'],result,key,model)
                    st.session_state['last_result']={'question':question,'sql':generated['sql'],
                        'result':result,'answer':answer}
        except Exception as exc:
            st.error('The request could not be completed. Check your API configuration or simplify the question.')
            with st.expander('Debug details'):
                st.code(str(exc))
                if generated and generated.get('sql'):
                    st.code(generated['sql'],language='sql')
if 'last_result' in st.session_state:
    last=st.session_state['last_result']
    st.subheader('Last successful question')
    st.write(last['question'])
    st.write(last['answer'])
    with st.expander('View SQL and database results'):
        st.code(last['sql'],language='sql')
        result=last['result']
        st.dataframe(pd.DataFrame(result['rows'],columns=result['columns']),hide_index=True)
        if result['truncated']:
            st.warning('Only the first 200 rows are displayed.')
