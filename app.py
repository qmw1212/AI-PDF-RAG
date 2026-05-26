"""PDF问答系统主应用"""
import os
# 必须在导入其他模块之前设置HuggingFace镜像
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

import streamlit as st
from pdf_processor import PDFProcessor
from vector_store import VectorStore
from gemini_client import GeminiClient


st.set_page_config(
    page_title="PDF问答系统",
    page_icon="📚",
    layout="wide"
)

st.title("📚 PDF问答系统")
st.markdown("上传PDF文档，然后提问相关问题")


@st.cache_resource
def initialize_components():
    """初始化系统组件"""
    with st.spinner("正在加载系统组件，首次运行需要下载模型，请稍候..."):
        pdf_processor = PDFProcessor(chunk_size=1000, chunk_overlap=200)
        vector_store = VectorStore(collection_name="pdf_documents")
        gemini_client = GeminiClient()
    return pdf_processor, vector_store, gemini_client


try:
    pdf_processor, vector_store, gemini_client = initialize_components()
except ValueError as e:
    st.error(f"初始化失败：{str(e)}")
    st.info("请创建.env文件并设置GOOGLE_API_KEY")
    st.stop()
except Exception as e:
    st.error(f"加载组件时出错：{str(e)}")
    st.info("如果是首次运行，可能需要下载嵌入模型（约90MB），请耐心等待")
    st.stop()


with st.sidebar:
    st.header("📄 上传PDF文档")

    uploaded_file = st.file_uploader(
        "选择PDF文件",
        type=['pdf'],
        help="上传你想要提问的PDF文档"
    )

    if uploaded_file is not None:
        if st.button("处理PDF", type="primary"):
            with st.spinner("正在处理PDF..."):
                try:
                    chunks = pdf_processor.process_pdf(uploaded_file)

                    vector_store.reset()
                    vector_store.add_documents(chunks)

                    st.session_state['pdf_processed'] = True
                    st.session_state['chunks_count'] = len(chunks)

                    st.success(f"✅ PDF处理完成！共分割为 {len(chunks)} 个文本块")
                except Exception as e:
                    st.error(f"处理PDF时出错：{str(e)}")

    if st.session_state.get('pdf_processed', False):
        st.info(f"📊 当前文档：{st.session_state.get('chunks_count', 0)} 个文本块")

        if st.button("清空文档"):
            vector_store.reset()
            st.session_state['pdf_processed'] = False
            st.session_state['chunks_count'] = 0
            st.rerun()


st.header("💬 提问")

if not st.session_state.get('pdf_processed', False):
    st.warning("⚠️ 请先上传并处理PDF文档")
else:
    question = st.text_input(
        "输入你的问题：",
        placeholder="例如：这个文档的主要内容是什么？"
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        n_results = st.number_input("检索块数", min_value=1, max_value=10, value=3)

    if st.button("🔍 提问", type="primary"):
        if question:
            with st.spinner("正在检索相关内容..."):
                relevant_chunks = vector_store.search(question, n_results=n_results)

            if relevant_chunks:
                with st.spinner("正在生成答案..."):
                    answer = gemini_client.generate_answer(question, relevant_chunks)

                st.subheader("📝 答案")
                st.write(answer)

                with st.expander("📄 查看检索到的相关内容"):
                    for i, chunk in enumerate(relevant_chunks, 1):
                        st.markdown(f"**片段 {i}:**")
                        st.text(chunk)
                        st.divider()
            else:
                st.warning("未找到相关内容")
        else:
            st.warning("请输入问题")


if 'pdf_processed' not in st.session_state:
    st.session_state['pdf_processed'] = False
