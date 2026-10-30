"""컴퓨팅 탐색 9주차: 강의의 데이터·그래프 예제를 확장한 Streamlit 앱.

실행: python -m streamlit run streamlit_app.py
"""

import numpy as np
import pandas as pd
import streamlit as st


# 1. 화면 설정
st.set_page_config(
    page_title="나의 데이터 실험실",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="auto",
)

st.markdown(
    """
    <style>
    .stApp { background: #f7f9fc; }
    .block-container { max-width: 1240px; padding-top: 2.4rem; }
    [data-testid="stSidebar"] { background: #edf3f5; }
    [data-testid="stSidebar"] .block-container { padding-top: 2rem; }
    h1 { letter-spacing: -0.055em; }
    h2, h3 { letter-spacing: -0.025em; }
    [data-testid="stMetric"] {
        background: #fff; border: 1px solid #dce5eb;
        border-radius: 14px; padding: 18px 22px;
    }
    [data-testid="stMetricValue"] { color: #136f63; }
    .eyebrow {
        color: #136f63; font-size: .78rem; font-weight: 700;
        letter-spacing: .13em; margin-bottom: .5rem;
    }
    .sidebar-note { color: #536777; font-size: .88rem; line-height: 1.7; }
    </style>
    """,
    unsafe_allow_html=True,
)


# 2. 데이터 재생성 버튼을 눌렀을 때만 난수 기준을 바꿉니다.
# 다른 위젯을 조작해도 같은 데이터를 비교할 수 있습니다.
if "data_seed" not in st.session_state:
    st.session_state.data_seed = 42

with st.sidebar:
    st.markdown("### 📊 데이터 실험실")
    st.caption("컴퓨팅 탐색 · WEEK 09")
    st.divider()
    st.markdown("#### 실험 설정")

    row_count = st.slider(
        "데이터 개수",
        min_value=10,
        max_value=100,
        value=20,
        step=10,
        help="강의 예제의 기본값은 20행입니다.",
        key="row_count",
    )
    selected_columns = st.multiselect(
        "그래프에 표시할 항목",
        options=["A", "B", "C"],
        default=["A", "B", "C"],
        key="selected_columns",
    )
    chart_type = st.radio(
        "그래프 종류",
        options=["꺾은선그래프", "막대그래프", "영역그래프"],
        key="chart_type",
    )

    if st.button("새 데이터 만들기", type="primary", width="stretch"):
        st.session_state.data_seed += 1

    st.caption(f"데이터 번호 · {st.session_state.data_seed - 41:02d}")
    st.divider()
    st.markdown(
        '<div class="sidebar-note">설정을 바꾸며 그래프를 비교해 보세요.<br>'
        '새 데이터 만들기를 누르면 새로운 값이 생성됩니다.</div>',
        unsafe_allow_html=True,
    )


# 3. 강의의 핵심: NumPy 난수 → pandas DataFrame
# 강의의 np.random.randn(20, 3)과 같은 표준정규분포를 사용합니다.
# seed를 지정해 화면 조작 중 데이터가 임의로 바뀌지 않게 합니다.
rng = np.random.default_rng(st.session_state.data_seed)
data = pd.DataFrame(
    rng.standard_normal((row_count, 3)),
    columns=["A", "B", "C"],
)
data.index = pd.RangeIndex(start=1, stop=row_count + 1, name="순서")
visible_data = data[selected_columns]


# 4. 제목과 안내
st.markdown('<div class="eyebrow">COMPUTING EXPLORATION / WEEK 09</div>',
            unsafe_allow_html=True)
st.title("나의 데이터 실험실")
st.write("데이터를 바꾸고, 그래프로 흐름을 발견해 보세요.")
st.caption("NumPy로 생성한 연습용 난수 데이터입니다. 실제 조사·관측 자료가 아닙니다.")
st.write("")


# 5. 요약 정보: 선택한 데이터에 맞추어 갱신됩니다.
col1, col2, col3 = st.columns(3)
col1.metric("데이터 개수", f"{row_count}행")
col2.metric("선택한 항목", f"{len(selected_columns)}개")
mean_value = f"{visible_data.to_numpy().mean():.3f}" if selected_columns else "—"
col3.metric("표시된 값의 평균", mean_value)
st.write("")

chart_tab, data_tab, lesson_tab = st.tabs(["데이터 흐름", "원본 데이터", "수업 코드"])


# 6. 강의의 핵심: st.line_chart(data)
with chart_tab:
    with st.container(border=True):
        st.subheader("숫자를 흐름으로 보기")
        st.caption(f"{row_count}개의 데이터 · 선택 항목: {', '.join(selected_columns) or '없음'}")

        if selected_columns:
            palette = {"A": "#168578", "B": "#ed9c43", "C": "#6c83d2"}
            colors = [palette[column] for column in selected_columns]
            chart_options = dict(
                height=360,
                x_label="데이터 순서",
                y_label="값",
                color=colors,
            )
            if chart_type == "꺾은선그래프":
                st.line_chart(visible_data, **chart_options)
            elif chart_type == "막대그래프":
                st.bar_chart(visible_data, **chart_options)
            else:
                st.area_chart(visible_data, **chart_options)
        else:
            st.info("왼쪽에서 그래프에 표시할 항목을 한 개 이상 선택해 주세요.")

    st.caption("읽는 방법 · 가로축은 데이터의 순서, 세로축은 생성된 값입니다. 색은 A·B·C 항목을 구분합니다.")
    with st.expander("이 데이터로 무엇을 살펴볼 수 있나요?"):
        st.write(
            "각 항목이 어느 지점에서 높거나 낮은지 비교해 보세요. "
            "그래프 종류를 바꾸면 같은 데이터도 다르게 보입니다. "
            "이 값은 무작위로 생성되므로 실제 현상의 원인이나 미래 추세를 설명하지는 않습니다."
        )


# 7. 원본 표와 다운로드
with data_tab:
    st.subheader("그래프 뒤의 숫자들")
    st.caption("현재 선택한 항목의 전체 데이터와 기초 통계입니다.")
    if selected_columns:
        st.dataframe(visible_data.style.format("{:.3f}"), width="stretch", height=380)
        st.download_button(
            label="선택한 데이터 CSV 다운로드",
            data=visible_data.to_csv(index=True).encode("utf-8-sig"),
            file_name="my_sample_data.csv",
            mime="text/csv",
        )
        st.markdown("#### 기초 통계")
        summary = visible_data.agg(["mean", "min", "max"]).rename(
            index={"mean": "평균", "min": "최솟값", "max": "최댓값"}
        )
        st.dataframe(summary.style.format("{:.3f}"), width="stretch")
    else:
        st.info("왼쪽에서 항목을 선택하면 표와 통계를 확인할 수 있습니다.")


# 8. 강의 예제를 그대로 확인할 수 있는 탭
with lesson_tab:
    st.subheader("강의에서 시작한 작은 웹앱")
    st.write("9주차 강의자료의 기본 예제입니다. 이 앱도 같은 순서로 동작합니다.")
    st.code(
        '''import streamlit as st
import pandas as pd
import numpy as np

st.title("간단한 Streamlit 예제")
st.write("데이터와 그래프를 보여주는 예제입니다.")

data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["A", "B", "C"]
)

st.line_chart(data)''',
        language="python",
    )
    st.write("이 화면에는 데이터 개수 조절, 항목 선택, 그래프 전환, 원본 표와 CSV 다운로드를 더했습니다.")

st.divider()
st.caption("컴퓨팅 탐색 9주차 · Python + Streamlit + pandas + NumPy")
