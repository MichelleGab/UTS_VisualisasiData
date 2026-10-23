import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
st.set_page_config(page_title="Gudeg Sekar Arum | Dashboard 2025", layout="wide")
st.title("Dashboard Penjualan — Gudeg Sekar Arum 2025")
st.caption("Data simulasi untuk proyek UTS Visualisasi Data; bukan transaksi usaha nyata.")
df = pd.read_excel(Path(__file__).parent / "Kelompok2_D5_Data_Dashboard.xlsx", sheet_name="Data_Bersih")
df["Tanggal"] = pd.to_datetime(df["Tanggal"])
bulan_id = {1:"Januari",2:"Februari",3:"Maret",4:"April",5:"Mei",6:"Juni",7:"Juli",8:"Agustus",9:"September",10:"Oktober",11:"November",12:"Desember"}
df["Bulan"] = df["Tanggal"].dt.month.map(bulan_id)
a,b,c = st.columns(3)
with a: o=st.selectbox("Outlet",["Semua"]+sorted(df["Outlet"].dropna().unique().tolist()))
with b: k=st.selectbox("Kanal penjualan",["Semua"]+sorted(df["Kanal_Penjualan"].dropna().unique().tolist()))
with c: m=st.selectbox("Bulan",["Semua"]+[bulan_id[i] for i in range(1,13)])
f=df.copy()
if o!="Semua": f=f[f["Outlet"]==o]
if k!="Semua": f=f[f["Kanal_Penjualan"]==k]
if m!="Semua": f=f[f["Bulan"]==m]
sales=f["Omzet_Bersih_Rp"].sum(); tx=f["Jumlah_Transaksi"].sum()
ticket=sales/tx if tx else 0
nrev=f["Jumlah_Ulasan"].sum()
rating=((f["Rating_Rata_rata"].fillna(0)*f["Jumlah_Ulasan"]).sum()/nrev) if nrev else 0
x1,x2,x3,x4=st.columns(4)
x1.metric("Omzet bersih",f"Rp{sales:,.0f}".replace(",","."))
x2.metric("Jumlah transaksi",f"{tx:,.0f}".replace(",","."))
x3.metric("Rata-rata per transaksi",f"Rp{ticket:,.0f}".replace(",","."))
x4.metric("Rating berbobot",f"{rating:.2f}/5" if nrev else "Tidak ada ulasan")
l,r=st.columns(2)
with l:
    ag=f.groupby("Outlet",as_index=False)["Omzet_Bersih_Rp"].sum().sort_values("Omzet_Bersih_Rp",ascending=False)
    st.plotly_chart(px.bar(ag,x="Omzet_Bersih_Rp",y="Outlet",orientation="h",title="Omzet bersih menurut outlet",labels={"Omzet_Bersih_Rp":"Omzet bersih (Rp)"}),use_container_width=True)
with r:
    ag=f.groupby("Kanal_Penjualan",as_index=False)["Omzet_Bersih_Rp"].sum().sort_values("Omzet_Bersih_Rp",ascending=False)
    st.plotly_chart(px.bar(ag,x="Kanal_Penjualan",y="Omzet_Bersih_Rp",title="Omzet bersih menurut kanal",labels={"Omzet_Bersih_Rp":"Omzet bersih (Rp)","Kanal_Penjualan":"Kanal"}),use_container_width=True)
l,r=st.columns(2)
with l:
    ag=f.groupby("Tanggal",as_index=False)["Omzet_Bersih_Rp"].sum()
    st.plotly_chart(px.line(ag,x="Tanggal",y="Omzet_Bersih_Rp",title="Tren omzet harian",labels={"Omzet_Bersih_Rp":"Omzet bersih (Rp)"}),use_container_width=True)
with r:
    ag=f.groupby("Outlet",as_index=False).agg(Wisatawan=("Transaksi_Wisatawan","sum"),Lokal=("Transaksi_Lokal","sum")).melt(id_vars="Outlet",var_name="Segmen",value_name="Transaksi")
    st.plotly_chart(px.bar(ag,x="Outlet",y="Transaksi",color="Segmen",barmode="stack",title="Transaksi menurut segmen"),use_container_width=True)
st.subheader("Data sesuai filter")
st.dataframe(f[["Tanggal","Outlet","Kanal_Penjualan","Jumlah_Transaksi","Transaksi_Wisatawan","Transaksi_Lokal","Omzet_Bersih_Rp","Rating_Rata_rata","Jumlah_Ulasan"]].head(1000),use_container_width=True)
st.caption("Data simulasi. Tanpa biaya/margin, laba dan ROI tidak dapat dihitung. Rating hanya tersedia pada record dengan ulasan.")
