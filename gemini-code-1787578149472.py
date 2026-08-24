import ast
import operator
import streamlit as st

st.set_page_config(page_title="SPACE_CALC v6.0", page_icon="🧮", layout="centered")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0c10;
        color: #66fcf1;
    }
    div[data-testid="stMetricValue"] {
        background-color: #1f2833;
        color: #66fcf1;
        font-family: 'Courier New', Courier, monospace;
        padding: 15px;
        border-radius: 5px;
        border: 2px solid #45a29e;
        font-size: 32px;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
        height: 60px;
        font-size: 20px !important;
        font-family: 'Courier New', Courier, monospace;
        font-weight: bold;
        background-color: #c5c6c7;
        color: #0b0c10;
        border: none;
        border-radius: 5px;
    }
    </style>
""",
    unsafe_allow_html=True,
)


def safe_eval(expr):
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def _eval(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](_eval(node.left), _eval(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](_eval(node.operand))
        else:
            raise TypeError("Ungueltig")

    parsed = ast.parse(expr, mode="eval")
    return _eval(parsed.body)


if "display" not in st.session_state:
    st.session_state.display = "0"
if "game_active" not in st.session_state:
    st.session_state.game_active = False

st.title("SPACE_CALC // v6.0")

st.metric(label="Eingabe / Ergebnis", value=st.session_state.display)


def press(val):
    if val == "C":
        st.session_state.display = "0"
        st.session_state.game_active = False
    elif val == "=":
        try:
            cleaned = st.session_state.display.replace(" ", "")

            if cleaned in ["67*67", "67*67.0"]:
                st.session_state.game_active = True

            res = safe_eval(cleaned)
            st.session_state.display = (
                str(int(res)) if res == int(res) else str(res)
            )
        except Exception:
            st.session_state.display = "ERROR"
    else:
        if (
            st.session_state.display == "0"
            or st.session_state.display == "ERROR"
        ):
            st.session_state.display = str(val)
        else:
            st.session_state.display += str(val)


buttons = [
    ["C", "(", ")", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["0", ".", "="],
]

for row in buttons:
    cols = st.columns(len(row))
    for idx, btn_text in enumerate(row):
        with cols[idx]:
            if st.button(btn_text, key=f"btn_{btn_text}"):
                press(btn_text)
                st.rerun()

if st.session_state.game_active:
    st.info("MARIO MINI-GAME EASTER EGG UNLOCKED!")
    st.success("Punkte: 1000! Du hast das Hindernis uebersprungen.")