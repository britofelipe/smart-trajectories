# **Smart Trajectories**

## **Funções Disponíveis**

- **`txt_to_csv(txt_filename, csv_filename)`**  
  Lê trajetórias de um arquivo de texto e grava os dados processados em um arquivo CSV.

- **`txt_to_csv_datetime(txt_filename, csv_filename)`**  
  Converte um arquivo de texto em CSV, incluindo a conversão de timestamps para objetos datetime.

- **`generate_trajectory_collection(filename)`**  
  Carrega um arquivo CSV e transforma os dados em uma coleção de trajetórias.

- **`plot_trajectories(traj_collection)`**  
  Plota todas as trajetórias de uma coleção no plano cartesiano.

- **`plot_trajectories_categorized(traj_collection)`**  
  Plota as trajetórias de uma coleção categorizadas por cores.

- **`plot_trajectories_one_category(traj_collection, category)`**  
  Plota as trajetórias de uma única categoria específica.

- **`plot_trajectories_with_background(traj_collection, background_image_path)`**  
  Plota as trajetórias sobre uma imagem de fundo estática.

- **`plot_trajectories_one_category_background(traj_collection, category, background_image_path)`**  
  Plota as trajetórias de uma categoria sobre uma imagem de fundo.

- **`plot_trajectories_with_limits(traj_collection, category, background_image_path)`**  
  Plota as trajetórias de uma categoria com a verificação de cruzamento de uma linha de referência.

- **`plot_trajectories_with_start_finish(traj_collection, category, background_image_path)`**  
  Plota as trajetórias de uma categoria verificando o início e fim correto da trajetória com linhas de partida e chegada.

---

## **Como Utilizar a Biblioteca `smart-trajectories`**

1. **Instalação**  
   Instale a biblioteca usando o comando:  
   ```bash
   python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps smart-trajectories
