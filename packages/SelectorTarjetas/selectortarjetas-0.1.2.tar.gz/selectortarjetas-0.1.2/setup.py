from setuptools import setup, find_packages

setup(
    name="SelectorTarjetas",
    version="0.1.2",
    description="Componente de Streamlit para mostrar tarjetas interactivas",
    author="Wilfrido CO",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # Incluye todo el contenido de la carpeta build dentro de tu paquete
        "selector_tarjetas": ["../frontend/build/*", "../frontend/build/static/**/*"]
    },
    install_requires=[
        "streamlit"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)