import streamlit as st
import pandas as pd

arq_hist = "historico.csv"

def calcular(vi, vm, pr,tx,mes_a_mes=False):
    hist_mont = []
    hist_juros = []
    mont = vi
    i = tx
    t = 1
    juros = 0
    while t <= pr:
        j = mont * i
        juros += j
        mont = mont + j + vm
        t += 1
        hist_mont.append(mont)
        hist_juros.append(juros)
    if mes_a_mes:
        return hist_mont, hist_juros
    else:
        return mont, juros

def adicionar_historico(vi, vm, pr,tx,mont, juros):
    linha = "%.2f,%.2f,%d,%.3f,%.2f,%.2f\n"%(vi, vm, pr,tx,mont, juros)
    with open(arq_hist,"a") as f:
        f.write(linha)

def limpar_historico():
    with open(arq_hist,"w") as f:
        f.write("Valor Inicial,Valor Mensal,Periodo,Taxa de Juros,Juros, Montante\n")

def format_input_data(vi, vm, pr, tx):
    vm = float(vm) if vm != "" else 0
    return float(vi), vm, int(pr), float(tx)

@st.dialog("Resultado")
def modal_resultado(mont, juros):
    st.write("Montante = R$ %.2f" % mont)
    st.write("Juros = R$ %.2f" % juros)

tab1, tab2 = st.tabs(["Calculadora", "Histórico"])
with tab1:
    st.header("Calculadora de Juros Compostos")
    vi = st.text_input("Valor inicial")
    vm = st.text_input("Valor mensal")
    tx = st.text_input("Taxa de juros mensal")
    pr = st.text_input("Período (em meses)")

    if st.button("Calcular"):
        if vi != "" and tx != "" and pr != "":
            vi, vm, pr, tx = format_input_data(vi, vm, pr, tx)
            mont, juros = calcular(vi, vm, pr, tx)
            modal_resultado(mont, juros)
            adicionar_historico(vi, vm, pr,tx,juros, mont)

    if st.button("Calcular mês a mês"):
        if vi != "" and tx != "" and pr != "":
            vi, vm, pr, tx = format_input_data(vi, vm, pr, tx)
            hist_mont, hist_juros = calcular(vi, vm, pr, tx, True)
            hist = {"Montante": hist_mont, "Juros": hist_juros}
            st.dataframe(pd.DataFrame(hist))
            st.area_chart(pd.DataFrame(hist))

with tab2:
    st.dataframe(pd.read_csv(arq_hist))
    if st.button("Limpar histórico"):
        limpar_historico()
        st.rerun()