botblocker
==========

Programa em Python para identificar e bloquear seus seguidores bots no Twitter

Requisitos: 3.4 <= Python <= 3.7

Começando
---------

Essas instruções vão te conseguir uma cópia do projeto rodando na sua máquina local para propósitos de desenvolvimento e testes apenas.

Instalando
~~~~~~~~~~

**Apenas se você estiver usando o Python >= 3.7, você vai ter de rodar esse comando antes:**

::

   sudo pip install https://github.com/tweepy/tweepy/archive/master.zip

Agora, independente da versão do Python (contanto que bata com os requisitos), a maneira mais fácil de instalar é usando o pip:

::

   sudo pip install botblocker

Você também pode clonar esse repositório usando o git:

::

   git clone https://github.com/yanorestes/botblocker.git
   cd botblocker
   python setup.py install

Preparação
----------

A princípio, configurar as coisas do botblocker pode parecer um pouco complicado demais.
Entretanto, seguir esse passo-a-passo vai te garantir um procedimento bem fácil!
De qualquer forma, essa parte "difícil" do tutorial só vai ter de ser feita uma vez ;)!

1 - Conseguindo sua Twitter Developer Account
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Já que eu estou disponibilizando o código completo desse projeto, eu não posso deixar vocês usarem minhas chaves de API, então vocês vão precisar pegar elas pra vocês mesmos. É assim que se faz:

-  Acesse `esse link <https://developer.twitter.com/en/apply/user>`__ para associar seu perfil com uma Developer Account
-  Clique em ``Continue``
-  Marque a opção “I am requesting access for my own personal use”
-  Digite seu username no campo abaixo
-  Selecione o país que você mora e clique em ``Continue``
-  Marque a opção “Consumer / end-user experience”
-  Na caixa de texto abaixo, digite algo similar com o exemplo a seguir (note que é melhor não copiar o texto por inteiro, para que sua aplicação seja aprovada mais rapidamente):

::

   The project I'm building aims to identify and block follower bots. It is based on programming language Python, using Tweepy to connect to Twitter API and Botometer to identify bots. The project gives the user mutiple options on identifying and blocking the bots, resulting in a clean and simple usage. Botometer analizes each profile basing itself on the tweets and the specs of the profile, to, then, calculate a result (a score from 0 to 5; the higher, the more likely it is that the profile is indeed a bot). None of the results are shared with anyone or kept with us.

-  Marque a opção ``No`` e clique em ``Continue``
-  Passe pelos termos de serviço e marque a opção "read and agree"
-  Clique em “Submit application”
-  Cheque sua caixa de entrada no email e confirme seu email
-  Espere sua Developer Account ser aprovada

2 - Pegando suas chaves de API do Twitter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assim que sua Developer Account for aprovada, você pode começar a criar sua aplicação:

-  Acesse `esse link <https://developer.twitter.com/en/apps/create>`__
   para registrar sua aplicação
-  Escolha um nome autêntico e prencha o primeiro campo de texto
-  Na caixa de texto abaixo, digite algo similar ao seguinte exemplo:

::

   Python program to identify and block your bot followers on Twitter.

-  Cole https://github.com/yanorestes/botblocker no campo de texto abaixo
-  Pule para a última caixa de texto da página e digite algo similar ao exemplo abaixo:

::

   The project I'm building aims to identify and block follower bots. It is based on programming language Python, using Tweepy to connect to Twitter API and Botometer to identify bots. The project gives the user mutiple options on identifying and blocking the bots, resulting in a clean and simple usage.

-  Clique em ``Create`` e confirme

Você será redirecionado para a página de sua aplicação. Então, faça o seguinte:

-  Acesse a aba “Keys and tokens”
-  Salve as duas chaves em "Consumer API keys" em algum lugar. A primeira é sua Consumer Key e a segunda sua Consumer Secret Key. Você vai precisar das duas depois, configurando o botblocker:

.. image:: https://cdn.pbrd.co/images/HEvDXKu.png

3 - Pegando sua chave de API do Mashape
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Com suas chaves de API do Twitter em mãos, você só vai precisar pegar sua chave de API do Mashape. Siga esses passos para fazer isso:

-  Acesse `esse link <https://market.mashape.com/>`__ e registre uma conta (eu recomendo registrar com o GitHub, mas há outras opções)
-  Se você tem um cartão de crédito disponível (**não se preocupe, você não terá que pagar nem um real**), acesse `esse link <https://market.mashape.com/OSoMe/botometer-pro>`__, clique em ``Pricing`` e se inscreva no Basic Free Plan. Se você não tem, você pode usar `esse link <https://market.mashape.com/OSoMe/botometer>`__. O primeiro vai (provavelmente) fazer o programa rodar mais rápido.
-  `Nesse link <https://market.mashape.com/OSoMe/botometer>`__, copie sua "X-Mashape-Key" pessoal no código de exemplo de request e salve-a em algum lugar:

.. image:: https://my.mixtape.moe/nqkagq.png

Usando
------

Agora é hora de finalmente rodar o botblocker! O botblocker irá passar por todos os seus seguidores calculando uma "pontuação de bot" para cada um. A pontuação vai de 0 a 5. Quanto mais alto a pontuação, mais chance há de que esse perfil seja de fato um bot. Por padrão, o botblocker vai bloquear automaticamente perfis detectados como bots.

Se você instalou o pacote usando o pip (recomendado!), você pode simplesmente rodar o botblocker pela linha de comando:

::

   botblocker [-h] [-c] [--noblock] [--saveallowlist] [--softblock] [--report] [-l {1,2,3}] -u USER [-v]

Esses são os parâmetros que você pode usar:

-  ``-h`` or ``--help`` - Mostra uma mensagem de ajuda e fecha
-  ``-c`` or ``--config`` - (Re)configura as configurações de uso. Pelo menos uma vez você terá que fazer isso.
-  ``--noblock`` - Não bloqueia ninguém automaticamente. Não recomendado, especialmente para perfis com muitos seguidores, já que você pode acabar perdendo todo o progresso do programa se fechar antes de finalizar.
-  ``--saveallowlist`` - Salva os usuários identificados como não-bots em uma allowlist. **Recomendado** (para acelerar o processo nos próximos usos).
-  ``--softblock`` - Aplica um soft block (bloqueia e desbloqueia o perfil logo em seguida)
-  ``-r`` or ``--report`` - Denuncia os perfis identificados como bots para o Twitter
-  ``-l {1,2,3}`` or ``-level {1,2,3}`` - Define o nível de rigorosidade usado para identificar os bots. O níbel 1 considera apenas bots com pontuação >= 4, o nível 2 (padrão) considera aqueles com pontuação >= 3 e o nível 3 considera todos aqueles com pontuação >= 2.5.
-  ``-u USER`` or ``-user USER`` - O username do Twitter pelo qual você quer rodar o botblocker. Obrigatório.
-  ``-v`` or ``--version`` - Pega a versão atual do botblocker

Você também pode rodar o programa direto pelo ``botblocker.py``:

::

   python -W ignore -m botblocker [-h] [-c] [--noblock] [--saveallowlist] [--softblock] [--report] [-l {1,2,3}] -u USER [-v]

Contribuindo
------------

Eu estou aceitando pull requests que melhorem a velocidade e/ou legibilidade do código. Sinta-se à vontade para contribuir como puder!

Autores
-------

-  **Yan Orestes** - *Trabalho inicial* -
   `yanorestes <https://github.com/yanorestes>`__

License
-------

Esse projeto é licenciado pela MIT License - veja o arquivo
`LICENSE <https://github.com/yanorestes/botblocker/blob/master/LICENSE.txt>`__
para mais detalhes.