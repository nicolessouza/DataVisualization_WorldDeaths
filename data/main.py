import pandas as pd
import streamlit as st
import plotly.express as px

# Importando base de dados 
df = pd.read_csv("./data/cause_of_deaths.csv")

# Pegando as principais causas de morte de cada país
dfDeathsCause = df.drop(columns=["Country/Territory", "Code", "Year"]).idxmax(axis=1)

# Inserir nova coluna "Top Cause" no dataframe original
df["Top Cause"] = dfDeathsCause

# Gráfico 1: Mapa mundi com a evolução da principal causa de morte de cada país ao longo dos anos

fig1 = px.choropleth(df,               
              locations="Code",               
              color="Top Cause",
              hover_name="Country/Territory",
              animation_frame="Year",
              projection="natural earth",
              width=880,
              height=500,
              template='plotly_white',
              color_discrete_sequence=['#0DF205',
                                    '#F20505',
                                    '#F2E205',
                                    '#0F570A',
                                    '#B31414',
                                    '#FF6A19',
                                    '#45DF97',
                                    '#E0128A',
                                    '#E843D1',
                                    '#6A40DE',
                                    '#C27B74']
)

fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig1.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

# Título da Página
st.write("""
# Cause of Deaths around the World
""")

# Título primeiro Grafo
st.write("""
### Principal cause of death in each country
""")

# Gráfico 1
st.write(fig1)

# Dataset auxiliar com apenas as causas de morte
dfCause = df.drop(columns=["Country/Territory","Top Cause", "Year"]).reset_index(drop=True)

# Agora usamos melt para transformar as colunas em linhas
dfCause = dfCause.melt(id_vars=["Code"], var_name="Cause", value_name="Deaths")

# Título do segundo gráfico
st.write("""
### Impact of the selected cause of death in each country (number of cases)
""")

# Dropdown para escolher a causa de morte de interesse
cause = st.selectbox("Select the cause of death", dfCause["Cause"].unique())

# Gráfico mapa mundi que mostra a evolução da doença escolhida
fig2 = px.choropleth(df,
                locations="Code",
                color=cause,
                hover_name="Country/Territory",
                animation_frame="Year",
                projection="natural earth",
                width=840,
                height=500,
                template='plotly_white',
                color_continuous_scale=px.colors.sequential.YlOrRd,
                range_color=[0, dfCause.loc[dfCause["Cause"] == cause]["Deaths"].max()]
)
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig2.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

st.write(fig2)

# Título do terceiro gráfico
st.write("""
### Evolution of each cause of death in selected country (number of cases)
""")

# Dropdown para escolher o país
country = st.selectbox("Select the country", df["Country/Territory"].unique())

# Dataset auxiliar para o país escolhido
dfSelected = df.loc[df["Country/Territory"] == country].drop(columns=["Country/Territory","Code","Top Cause"]).reset_index(drop=True)

# Agora usamos melt para transformar as colunas em linhas
dfSelected = dfSelected.melt(id_vars=["Year"], var_name="Cause", value_name="Deaths")

# Gráfico de barras que mostra o número de mortes de cada doença para o país selecionado
fig3 = px.bar(dfSelected,
            x="Deaths",
            y="Cause",
            color="Cause",
            animation_frame="Year",
            # barmode="group",
            width=600,
            height=580,
            template='plotly_white',
            color_discrete_sequence=px.colors.qualitative.Light24
)
fig3.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig3.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

#não exibir legenda das cores
fig3.update_layout(showlegend=False)

#não exibir título dos eixos
fig3.update_xaxes(title_text='')
fig3.update_yaxes(title_text='')

# Terceiro Gráficos
st.write(fig3)

