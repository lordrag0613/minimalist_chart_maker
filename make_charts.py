import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Liste de palettes prédéfinies disponibles dans Plotly
predefined_palettes = {
    "Viridis": px.colors.sequential.Viridis,
    "Cividis": px.colors.sequential.Cividis,
    "RdBu": px.colors.diverging.RdBu,
    "Set": px.colors.qualitative.Set1,
    "Bis": px.colors.qualitative.Set2
}

# Fonction pour afficher un aperçu des couleurs de la palette
def show_palette_preview(palette):
    fig = go.Figure(go.Bar(
        x=list(range(len(palette))),
        y=[1] * len(palette),
        marker=dict(color=palette)
    ))
    fig.update_layout(
        height=100, 
        margin=dict(t=0, b=0, l=0, r=0), 
        xaxis=dict(showgrid=False, zeroline=False, visible=False),
        yaxis=dict(showgrid=False, zeroline=False, visible=False)
    )
    st.plotly_chart(fig, use_container_width=True)


st.title("📊 Création de graphiques minimaliste")

# Upload CSV ou Excel
uploaded_file = st.file_uploader("📂 Charge ton fichier CSV ou Excel", type=["csv", "xlsx"])

if uploaded_file:
    # Lire le fichier selon son format
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    st.write("📝 Aperçu des données :")
    st.dataframe(df)

    st.sidebar.header("🎛️ Paramètres du Graphique")
    chart_type = st.sidebar.selectbox("📊 Type de graphique", [
        "Nuage de points", 
        "Courbe", 
        "Barres", 
        "Camembert", 
        "Histogramme"
    ])

    selected_palette = st.sidebar.selectbox(
    "🎨 Choisissez une palette de couleurs", list(predefined_palettes.keys())
    )

    columns = df.columns.tolist()
    numeric_columns = df.select_dtypes(include=['number']).columns.tolist()

    x_col = st.sidebar.selectbox("Colonne X", columns)
    y_col = st.sidebar.selectbox("Colonne Y", numeric_columns)

    color_col = st.sidebar.selectbox("🎨 Colonne de différenciation (optionnel)", ["Aucune"] + columns)
    color_col = None if color_col == "Aucune" else color_col

    # Affichage du graphique
    if chart_type == "Nuage de points":
        fig = px.scatter(df, x=x_col, y=y_col, color=color_col, color_discrete_sequence=predefined_palettes[selected_palette])

    elif chart_type == "Courbe":
        sorted_df = df.sort_values(by=x_col)
        fig = px.line(sorted_df, x=x_col, y=y_col, color=color_col, color_discrete_sequence=predefined_palettes[selected_palette])

    elif chart_type == "Barres":
        st.sidebar.subheader("📊 Choix de l'agrégat")

        agg_dict = {
            "Somme": "sum",
            "Moyenne": "mean",
            "Nombre": "count",
            "Maximum": "max",
            "Minimum": "min"
        }

        agg_func = st.sidebar.selectbox("Fonction d'agrégation", list(agg_dict.keys()))
                                        
        if agg_func == "count":
            agg_df = df.groupby(x_col).size().reset_index(name='count')
            fig = px.bar(agg_df, x=x_col, y='count', color=color_col, color_discrete_sequence=predefined_palettes[selected_palette])
        else:
            agg_df = df.groupby(x_col)[y_col].agg(agg_dict[agg_func]).reset_index()
            fig = px.bar(agg_df, x=x_col, y=y_col, color=color_col, color_discrete_sequence=predefined_palettes[selected_palette])

    elif chart_type == "Histogramme":
        bins = st.sidebar.slider("Nombre de classes (bins)", min_value=5, max_value=100, value=20)
        fig = px.histogram(df, x=x_col, color=color_col, nbins=bins)
    if chart_type == "Camembert":
        pie_data = df[x_col].value_counts().reset_index()
        pie_data.columns = [x_col, 'count']
        fig = px.pie(pie_data, names=x_col, values='count', color_discrete_sequence=predefined_palettes[selected_palette])


    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("📄 Importez un fichier CSV pour commencer.")
