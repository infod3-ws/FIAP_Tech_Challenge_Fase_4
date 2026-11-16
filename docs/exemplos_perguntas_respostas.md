# Exemplos de perguntas e respostas

Gerado automaticamente por `python -m voc.run_examples`.

```text

PERGUNTA: Quais são os principais problemas relatados pelos clientes em suas avaliações?
  consulta reescrita: problemas com o produto, produto veio com defeito, entrega atrasou, atendimento ruim, não recebi o pedido, produto não correspondeu ao esperado
  filtros: nota>=3

RESPOSTA:
1. **Produto entregue errado**: Várias avaliações mencionam que os clientes receberam produtos diferentes do que compraram, como em [R1], [R10] e [R11].

2. **Produto com defeito**: Há relatos de produtos que chegaram com defeito, como em [R2], [R5] e [R9].

3. **Atraso na entrega**: Alguns clientes expressaram insatisfação com atrasos na entrega, como em [R2] e [R8].

4. **Expectativas não atendidas**: Avaliações indicam que alguns produtos não corresponderam às expectativas dos clientes, como em [R3] e [R6].

5. **Falta de itens na entrega**: Um cliente relatou que o produto veio faltando, conforme [R12].

6. **Problemas de comunicação**: Em algumas avaliações, os clientes mencionaram a falta de retorno do fornecedor após a reclamação, como em [R5].

EVIDÊNCIAS (✔ = citada na resposta):
 ✔ [R1] nota 3 | sim=0.7 | 2018-05 | beleza saude | review_id=256869e0…
       "Produto entregue errado. Produto entregue errado, ainda não recebi o que comprei"
 ✔ [R2] nota 3 | sim=0.698 | 2018-07 | informatica acessorios | review_id=a9d65ad2…
       "O produto veiocom defeito. O produto veio com defeito e atraso na entrega"
 ✔ [R3] nota 3 | sim=0.693 | 2017-02 | ferramentas jardim | review_id=7ef89214…
       "Recebi o produto dentro do prazo, mas o produto deixou muito a desejar, muito frágil, não atendeu as expectativas"
 ✔ [R5] nota 4 | sim=0.681 | 2017-09 | pcs | review_id=714f4894…
       "Embora recebi o produto correto e no prazo o produto veio com Defeito. Estou aguardando o contato do fornecedor para efetuar a troca"
 ✔ [R6] nota 4 | sim=0.68 | 2017-02 | brinquedos | review_id=86e9daec…
       "olá , meu produto foi entregue , muito antes do prazo . minha queixa é apenas pelo produto não ter sido aquilo que eu esperava"
 ✔ [R8] nota 3 | sim=0.674 | 2018-03 | instrumentos musicais | review_id=529dc319…
       "produto bom. produto conforme o especificado, mas a entrega via correios foi péssima, o produto levou quase um mês perdido até ser entregue"
 ✔ [R9] nota 5 | sim=0.673 | 2017-03 | telefonia | review_id=211b5045…
       "o produto veio com defeito. ja mandei email reclamando"
 ✔ [R10] nota 4 | sim=0.668 | 2017-04 | utilidades domesticas | review_id=41399851…
       "Recebi um produto que não veio conforme eu pedi, recebi outro"
 ✔ [R11] nota 5 | sim=0.667 | 2018-08 | fashion bolsas e acessorios | review_id=39b0f45c…
       "O produto veio errado, isso acontece"
 ✔ [R12] nota 3 | sim=0.665 | 2017-10 | consoles games | review_id=644926b1…
       "Comprei um produto e veio faltando na entrega"
```

```text

PERGUNTA: O que os clientes relatam sobre problemas relacionados à entrega?
  consulta reescrita: problemas com a entrega, produto não chegou, entrega atrasou, demorou muito para receber o pedido, pedido extraviado
  filtros: nenhum

RESPOSTA:
1. Muitos clientes relatam demora significativa na entrega dos produtos, como evidenciado em avaliações que mencionam "muita demora na entrega" [R1][R5] e "produto foi entregue com muita demora" [R3].

2. Há casos de produtos que não foram entregues, como indicado nas avaliações que afirmam "a mercadoria não foi entregue" [R2] e "o produto não chegou" [R9].

3. Problemas de extravio também são mencionados, com um cliente relatando que "a encomenda extraviou" [R4].

4. A falta de comunicação sobre o status da entrega é uma preocupação, com clientes reclamando que "não dão satisfação" [R7] e que "não fui avisada sobre a entrega" [R8].

5. Alguns clientes reconhecem que atrasos podem ser atribuídos a problemas externos, como "os correios estavam com problemas" [R6].

6. Em geral, as avaliações refletem uma insatisfação significativa com o processo de entrega, com várias menções a atrasos e produtos não recebidos.

EVIDÊNCIAS (✔ = citada na resposta):
 ✔ [R1] nota 1 | sim=0.715 | 2018-04 | utilidades domesticas | review_id=4418b704…
       "muita demora na entrega, produtos comprados com os demais chegaram à muito tempo"
 ✔ [R2] nota 2 | sim=0.693 | 2017-09 | malas acessorios | review_id=ebc75dc1…
       "tive problemas com a entrega a mercadoria não foi entrgue"
 ✔ [R3] nota 2 | sim=0.682 | 2017-07 | bebes | review_id=6bccb495…
       "Produto foi entregue com muita demora"
 ✔ [R4] nota 1 | sim=0.682 | 2018-01 | relogios presentes | review_id=4355e137…
       "O produto demorou a ser enviado. Quando foi, a encomenda extraviou. Era pra presente"
 ✔ [R5] nota 2 | sim=0.682 | 2017-12 | beleza saude | review_id=d769d6d2…
       "muita demora na entrega, levou mais de 15 dias pra entregar e mesmo assim so entregou um dos produtos que eu fiz"
 ✔ [R6] nota 4 | sim=0.678 | 2017-05 | eletroportateis | review_id=2c8911a9…
       "Houve atraso na entrega do produto, porém os correios estavam com problemas"
 ✔ [R7] nota 1 | sim=0.678 | 2018-03 | telefonia | review_id=91c3523e…
       "muita demora na entrega, não dão satisfação"
 ✔ [R8] nota 1 | sim=0.677 | 2018-05 | relogios presentes | review_id=c82e20ab…
       "muitos problemas na entrega do mesmo. não fui avisada sobre a entrega"
 ✔ [R9] nota 1 | sim=0.676 | 2018-01 | brinquedos | review_id=3bd4d54b…
       "Houve algum problema na entrega e o produto não chegou"
```

```text

PERGUNTA: Quais aspectos da experiência de compra são mais elogiados pelos clientes?
  consulta reescrita: o que os clientes mais elogiam na experiência de compra, atendimento excelente, entrega rápida, facilidade de navegação no site, qualidade dos produtos
  filtros: nota>=4

RESPOSTA:
1. **Segurança do site**: Vários clientes mencionam que o site é seguro para compras, como destacado em [R1] e [R12].

2. **Agilidade na navegação**: A facilidade de navegação pelo site é elogiada em avaliações como [R3] e [R7].

3. **Cumprimento de prazos**: A entrega no prazo é um aspecto frequentemente elogiado, conforme observado em [R2], [R4] e [R9].

4. **Qualidade dos produtos**: Muitos clientes ressaltam a qualidade dos produtos recebidos, como em [R5], [R8] e [R10].

5. **Atendimento ao cliente**: O atendimento é destacado como excelente em várias avaliações, incluindo [R6] e [R11].

6. **Praticidade da compra**: A experiência de compra é considerada prática e satisfatória, conforme mencionado em [R7] e [R9].

EVIDÊNCIAS (✔ = citada na resposta):
 ✔ [R1] nota 5 | sim=0.713 | 2018-02 | papelaria | review_id=76f56d42…
       "O site é seguro, a navegação é ágil, os parceiros, confiáveis, os produtos são honestos e sempre entregam antes do prazo"
 ✔ [R2] nota 5 | sim=0.711 | 2018-01 | perfumaria | review_id=d9921985…
       "melhor atendimento, entrega no prazo ,enfim melhor site para se comprar"
 ✔ [R3] nota 5 | sim=0.702 | 2018-01 | fashion underwear e moda praia | review_id=ccf42999…
       "Fácil navegação pelo site e cumprimento de tudo que fora solicitado (produto correto, sem violação da embalagem, prazo respeitado)"
 ✔ [R4] nota 5 | sim=0.697 | 2018-02 | cama mesa banho | review_id=d51f6b2e…
       "Ótimo site e loja, produto entegue rapido e com qualidade ótima"
 ✔ [R5] nota 5 | sim=0.693 | 2017-08 | telefonia | review_id=5b0484f3…
       "Ótimo e recomendado, prazo cumprido,produtos de qualidade e atendimento excelente"
 ✔ [R6] nota 5 | sim=0.691 | 2018-01 | cama mesa banho | review_id=cd57254f…
       "Atendimento e compromisso com o cliente excelente...sou cliente à muitos anos e nada tenho a reclamar, ótimo site de compras!! 😍"
 ✔ [R7] nota 5 | sim=0.685 | 2017-06 | pet shop | review_id=000da26f…
       "Muito satisfeita com o produto, entrega e a praticidade do site"
 ✔ [R8] nota 5 | sim=0.683 | 2017-10 | cama mesa banho | review_id=4cc3ab81…
       "entrega rápida , produto de qualidade, e preço bom"
 ✔ [R9] nota 5 | sim=0.681 | 2018-01 | ferramentas jardim | review_id=e92da858…
       "O site que mais gosto de compra. Produtos de qualidade, preço bom e as entregas sempre acorrem antes mesmo da data prevista!"
 ✔ [R10] nota 5 | sim=0.68 | 2017-08 | consoles games | review_id=985234d8…
       "Otimos produtos otima entrega só elogios"
 ✔ [R11] nota 5 | sim=0.68 | 2018-01 | informatica acessorios | review_id=6cc7ced4…
       "otimo atendimento, otima mercadoria"
 ✔ [R12] nota 4 | sim=0.68 | 2018-02 | esporte lazer | review_id=ae557f46…
       "Site super seguro pra compra e com entrega garantida, além de produtos com excelente qualidade"
```

```text

PERGUNTA: Quais padrões podem ser identificados nas avaliações de clientes insatisfeitos?
  consulta reescrita: clientes insatisfeitos, reclamações, problemas com o produto, atendimento ruim, entrega atrasada, produto não chegou, qualidade do produto ruim
  filtros: nota>=1 nota<=3

RESPOSTA:
1. **Problemas de entrega**: Várias avaliações mencionam a não entrega dos produtos, como em [R2], [R7] e [R9], onde os clientes expressam frustração pela falta de satisfação e comunicação sobre o status das entregas.

2. **Qualidade do produto**: A insatisfação com a qualidade dos produtos é um padrão recorrente, com clientes relatando produtos de baixa qualidade em avaliações como [R1], [R3] e [R10].

3. **Falta de suporte ao cliente**: Muitos clientes reclamam da ausência de canais de reclamação ou ouvidoria, como destacado em [R2] e [R5], o que agrava a insatisfação.

4. **Atrasos sem comunicação**: Atrasos na entrega sem qualquer informação ao cliente são mencionados em avaliações como [R6] e [R8], indicando uma falta de consideração com o consumidor.

5. **Problemas com embalagem e devolução**: Avaliações como [R5] indicam insatisfação com a embalagem dos produtos e dificuldades em realizar devoluções, o que contribui para a frustração do cliente.

6. **Desconformidade com a descrição do produto**: Há relatos de produtos que não correspondem à descrição apresentada, como em [R11], o que gera descontentamento entre os clientes.

EVIDÊNCIAS (✔ = citada na resposta):
 ✔ [R1] nota 1 | sim=0.746 | 2018-07 | automotivo | review_id=190b01af…
       "produto insatisfatorio. demora na entrega e produto de baixa qualidade"
 ✔ [R2] nota 1 | sim=0.705 | 2018-08 | informatica acessorios | review_id=8ff6181c…
       "Produto não entregue. Tudo muito ruim, não tem ninguém com possamos fazer reclamação pela não entrega do do produto. Não tem ouvidoria, para reclamações. Não tem nenhum pessypara informar o por que da demora da entrega"
 ✔ [R3] nota 1 | sim=0.681 | 2018-08 | relogios presentes | review_id=f5eb1bfa…
       "Insatisfação. Não estou satisfeita com a qualidade do produto"
 ✔ [R5] nota 1 | sim=0.676 | 2017-03 | alimentos | review_id=6d096d02…
       "Falta de respeito com consumidor; produto mal embalado, vidros sem lacre vazando; náo recebi autorização de devolução, mesmo tendo reclamado no dia da entrega; o pior, terei que levar ao correio"
 ✔ [R6] nota 1 | sim=0.665 | 2017-12 | moveis decoracao | review_id=2d0a0700…
       "Atraso na entrega sem dar satisfação ao cliente, que com certeza escolheu o produto com cuidado e com as melhores expectativas. Falta de consideração"
 ✔ [R7] nota 1 | sim=0.664 | 2017-12 | beleza saude | review_id=4966a0af…
       "Falta de compromisso com o cliente. O meu produto nunca chegou apesar das minhas reclamações"
 ✔ [R8] nota 1 | sim=0.663 | 2017-06 | cama mesa banho | review_id=949eca02…
       "muitos desencontros nas entregas de produtos"
 ✔ [R9] nota 1 | sim=0.655 | 2018-08 | desconhecida | review_id=8672a30c…
       "Produto não entregue. Produto não entregue e sem dar satisfação ao cliente"
 ✔ [R10] nota 1 | sim=0.654 | 2018-06 | telefonia | review_id=1060d56d…
       "produto ruim. produto de má qualidade"
 ✔ [R11] nota 1 | sim=0.646 | 2018-07 | moveis decoracao | review_id=16230daf…
       "Insatisfeita. Produto recebido com riscos, descrição do produto não condiz com a realidade"
```

```text

PERGUNTA: Quais avaliações sustentam a conclusão de que existem problemas recorrentes de prazo de entrega?
  consulta reescrita: atraso na entrega, produto chegou depois do prazo, demorou muito para receber, entrega não foi no tempo certo
  filtros: nota<=3

RESPOSTA:
As avaliações que sustentam a conclusão de que existem problemas recorrentes de prazo de entrega são:

1. Várias avaliações mencionam atrasos significativos na entrega, como em [R1], onde o cliente relata que a mercadoria não cumpriu o prazo determinado.
2. A avaliação [R4] destaca que o produto foi entregue muito fora do prazo, indicando um problema recorrente.
3. Em [R5], o cliente menciona "muita demora na entrega", reforçando a insatisfação com os prazos.
4. A avaliação [R6] também aponta que o produto foi entregue após o prazo estimado, mesmo com pagamento de frete.
5. A insatisfação com prazos longos é evidente em [R8], onde o cliente reclama que o produto não chegou no prazo.
6. Por fim, [R10] relata que o cliente ainda não recebeu o produto após o prazo solicitado, evidenciando a continuidade do problema.

EVIDÊNCIAS (✔ = citada na resposta):
 ✔ [R1] nota 1 | sim=0.804 | 2018-08 | cama mesa banho | review_id=10467dc4…
       "atraso na entrega da mercadoria,não cumpre prazo determinado"
   [R2] nota 3 | sim=0.796 | 2017-02 | perfumaria | review_id=328ce2c5…
       "Embora o produto foi entregue dentro do prazo, demorou muito para ser entregue"
   [R3] nota 2 | sim=0.783 | 2017-09 | cama mesa banho | review_id=3463ea11…
       "O produto foi entregue corretamente, mas achei o prazo de entrega muito, mas muito demorado"
 ✔ [R4] nota 1 | sim=0.774 | 2017-06 | cool stuff | review_id=d445c6c8…
       "o produto só foi entregue bem fora do prazo"
 ✔ [R5] nota 1 | sim=0.774 | 2018-04 | utilidades domesticas | review_id=4418b704…
       "muita demora na entrega, produtos comprados com os demais chegaram à muito tempo"
 ✔ [R6] nota 1 | sim=0.773 | 2018-08 | moveis decoracao | review_id=02d90afe…
       "Atraso na entrega. Ainda recebi o produto,já passou do prazo estimado e paguei o frete"
 ✔ [R8] nota 1 | sim=0.767 | 2017-12 | cama mesa banho | review_id=8b592f04…
       "prazo longo de entrega e não chegou no prazo"
 ✔ [R10] nota 1 | sim=0.766 | 2018-08 | esporte lazer | review_id=0162340d…
       "Atraso na entrega. Ainda não recebi o produto é já se passou o prazo solicitado"
```

```text

PERGUNTA: Quais são os principais problemas nas avaliações com nota 1?
  consulta reescrita: problemas nas avaliações com nota 1, reclamações, insatisfações, produto com defeito, atendimento ruim, entrega atrasada
  filtros: nota>=1 nota<=1

RESPOSTA:
1. **Atraso na entrega**: Muitas avaliações mencionam atrasos significativos na entrega dos produtos, como em [R2], [R3], [R8] e [R10].

2. **Falta de comunicação**: Há uma clara insatisfação com a falta de informações sobre o status da entrega, conforme indicado em [R1], [R8] e [R11].

3. **Produto não entregue**: Várias avaliações relatam que os produtos nunca foram entregues, como em [R1] e [R11].

4. **Problemas com a qualidade do produto**: Avaliações como [R3] e [R5] destacam a insatisfação com a qualidade dos produtos recebidos, incluindo itens avariados.

5. **Dificuldade em realizar reclamações**: Os clientes expressam frustração com a falta de canais adequados para registrar reclamações, conforme observado em [R1] e [R12].

6. **Erro na entrega**: Há relatos de erros na entrega, como em [R7], onde o cliente menciona que o produto foi entregue incorretamente.

EVIDÊNCIAS (✔ = citada na resposta):
 ✔ [R1] nota 1 | sim=0.693 | 2018-08 | informatica acessorios | review_id=8ff6181c…
       "Produto não entregue. Tudo muito ruim, não tem ninguém com possamos fazer reclamação pela não entrega do do produto. Não tem ouvidoria, para reclamações. Não tem nenhum pessypara informar o por que da demora da entrega"
 ✔ [R2] nota 1 | sim=0.679 | 2018-03 | moveis escritorio | review_id=045d330f…
       "Nao tem boa avaliação por atraso na entrega"
 ✔ [R3] nota 1 | sim=0.678 | 2018-07 | automotivo | review_id=190b01af…
       "produto insatisfatorio. demora na entrega e produto de baixa qualidade"
 ✔ [R5] nota 1 | sim=0.67 | 2017-03 | alimentos | review_id=6d096d02…
       "Falta de respeito com consumidor; produto mal embalado, vidros sem lacre vazando; náo recebi autorização de devolução, mesmo tendo reclamado no dia da entrega; o pior, terei que levar ao correio"
 ✔ [R7] nota 1 | sim=0.653 | 2018-03 | fashion calcados | review_id=30db73d0…
       "houve erro na entrega do produto. Espero que tudo se regulariza para poder mudar minha avaliação atual"
 ✔ [R8] nota 1 | sim=0.652 | 2017-12 | moveis decoracao | review_id=2d0a0700…
       "Atraso na entrega sem dar satisfação ao cliente, que com certeza escolheu o produto com cuidado e com as melhores expectativas. Falta de consideração"
 ✔ [R10] nota 1 | sim=0.646 | 2018-03 | telefonia | review_id=91c3523e…
       "muita demora na entrega, não dão satisfação"
 ✔ [R11] nota 1 | sim=0.642 | 2017-12 | beleza saude | review_id=4966a0af…
       "Falta de compromisso com o cliente. O meu produto nunca chegou apesar das minhas reclamações"
 ✔ [R12] nota 1 | sim=0.641 | 2018-04 | cama mesa banho | review_id=3d163199…
       "Depois de receber o produto avariado e solicitar a troca,começou a enrolação.Tamanha falta de comunicação entre a loja e o fornecedor do produto. Em NENHUM momento houve convergência de informações"
```

```text

PERGUNTA: Qual é a capital da França?
  consulta reescrita: 
  filtros: nenhum

RESPOSTA:
NÃO HÁ EVIDÊNCIAS SUFICIENTES: a pergunta está fora do escopo da base (avaliações de clientes).
```

```text

PERGUNTA: Qual será o faturamento da empresa em 2027?
  consulta reescrita: 
  filtros: nenhum

RESPOSTA:
NÃO HÁ EVIDÊNCIAS SUFICIENTES: a pergunta está fora do escopo da base (avaliações de clientes).
```

```text

PERGUNTA: O que os clientes dizem sobre o sabor das pizzas?
  consulta reescrita: sabor das pizzas, pizza estava deliciosa, pizza muito boa, pizza sem gosto, pizza estava ruim
  filtros: nenhum

RESPOSTA:
NÃO HÁ EVIDÊNCIAS SUFICIENTES: encontrei apenas 2 avaliação(ões) relevante(s) (mínimo exigido: 5).

EVIDÊNCIAS (✔ = citada na resposta):
   [R1] nota 3 | sim=0.538 | 2017-06 | esporte lazer | review_id=42267fd4…
       "O sabor solicitado não condiz com o produto que foi entregue"
   [R2] nota 3 | sim=0.534 | 2018-02 | esporte lazer | review_id=a34f8fc3…
       "Foi tudo perfeito, tirando o sabor do produto que pedi baunilha e veio chocolate. Mas como não ligo mto pra isso e o sabor não tem tanta importância pra mim, nem liguei"
```
