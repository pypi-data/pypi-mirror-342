# socialdataanalysis

**Funções personalizadas para análise de dados nas ciências sociais, complementando o uso do SPSS, JASP, Jamovi e IBM-SPSS.**

Este pacote oferece uma coleção de funções úteis para análise de dados, especialmente projetadas para complementar as capacidades de softwares estatísticos populares em pesquisas nas ciências sociais e da saúde. As funções incluídas cobrem diversos aspectos da análise estatística, conforme descrito no livro [Análise de Dados para Ciências Sociais e da Saúde: A Complementaridade do Python, Jasp, Jamovi e IBM-SPSS](https://ciencia.iscte-iul.pt/publications/analise-de-dados-para-ciencias-sociais-e-da-saude--a-complementaridade-do-python-jasp-jamovi-e-ibm/104320).

## Recursos

- **Aquisição de Dados**: Download e carregamento de arquivos SAV.
- **Tratamento de Dados Ausentes**: Imputação múltipla e análise de padrões de valores ausentes.
- **Pré-processamento de Dados**: Transformações de escalas, padronização e ponderação de casos.
- **Análise Exploratória de Dados**: Estatísticas descritivas, tabelas de frequências e testes de normalidade.
- **Análise de Associação**: Qui-quadrado, razão de chances e análise de tabelas de contingência.
- **Análise Fatorial Exploratória**: Testes de esfericidade, KMO, extração de fatores e cargas fatoriais.
- **Análise de Cluster**: Métodos hierárquicos e K-Means.
- **Regressão Logística**: Modelos binários, multinomiais e ordinais.

## Instalação

Você pode instalar o pacote diretamente do PyPI usando pip:

```bash
pip install socialdataanalysis
```

## Uso

Aqui está um exemplo de como usar este pacote em um script Python:

```python
import pandas as pd
from socialdataanalysis.exploratorydataanalysis import gerar_tabela_estatisticas_descritivas

# DataFrame exemplo
data = {
    'variable_1': [10, 20, 30, 40, 50],
    'variable_2': [15, 25, 35, 45, 55],
    'variable_3': [20, 30, 40, 50, 60]
}

df = pd.DataFrame(data)

# Exemplo de uso
gerar_tabela_estatisticas_descritivas(df=df, variaveis=['variable_1', 'variable_2', 'variable_3'])
```

## Módulos Disponíveis

O pacote contém os seguintes módulos:

- `dataacquisition.py`: Aquisição de dados, incluindo download e leitura de arquivos .sav.
- `datamissingtreatment.py`: Tratamento de dados ausentes com testes e imputação.
- `datapreprocessing.py`: Transformações e padronização de dados.
- `exploratorydataanalysis.py`: Estatísticas descritivas e testes exploratórios.
- `association.py`: Análises de associação e testes de independência.
- `exploratoryfactoranalysis.py`: Análise fatorial exploratória e testes de adequação.
- `clusteranalysis.py`: Métodos de clustering hierárquico e K-Means.
- `logisticregression.py`: Modelos de regressão logística para variáveis binárias e multinomiais.

## Notebooks

Este pacote inclui notebooks de exemplo para demonstrar o uso das funções. Eles podem ser encontrados na pasta `notebooks` do repositório GitHub do projeto.

## Contribuição

Se você deseja contribuir para este projeto, por favor, envie um pull request. Para problemas ou sugestões, utilize o issue tracker no GitHub.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Autores

- Ricardo Coser Mergulhão - [ricardomergulhao@gmail.com](mailto:ricardomergulhao@gmail.com)
- Maria Helena Pestana - [gageiropestana@gmail.com](mailto:gageiropestana@gmail.com)
- Maria de Fátima Pina - [mariafatimadpina@gmail.com](mailto:mariafatimadpina@gmail.com)

## Agradecimentos

Agradecimentos especiais a todos os colaboradores e usuários deste pacote.
