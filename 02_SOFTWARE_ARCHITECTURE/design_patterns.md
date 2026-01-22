# Padrões de Projeto e Escalabilidade
- **Strategy Pattern:** O Core será agnóstico. Cada ramo (Agro, Saúde) será uma "Strategy" que implementa uma interface comum. Isso permite adicionar novos ramos sem alterar o motor principal.
- **Factory Method:** Responsável por instanciar o motor correto baseado no metadado do arquivo.
- **API First:** Comunicação entre módulos via interfaces definidas, permitindo que o processamento mude de Python para outra linguagem sem quebrar o Frontend.
