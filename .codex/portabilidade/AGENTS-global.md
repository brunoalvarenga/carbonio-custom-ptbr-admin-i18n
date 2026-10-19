# Encerramento de ambientes locais de teste

Preferência do usuário registrada em 14/10/2026. Aplica-se aos projetos deste computador.

- Antes de iniciar Colima, Docker ou outra VM local, identifique e informe o projeto, o perfil da VM e a finalidade. Não trate um serviço em execução como prova de que ainda é necessário.
- Use somente os serviços e o paralelismo necessários ao teste. Não inicie uma pilha completa ou muitas réplicas de workers quando um teste menor resolver a tarefa.
- Ao concluir o trabalho ou os testes de um projeto, encerre seus contêineres de teste e desligue a VM dedicada com parada graciosa. Não deixe testes, workers ou VMs em segundo plano após a entrega sem pedido explícito do usuário.
- Antes de desligar uma VM compartilhada, confira se outro trabalho ainda depende dela. Se não houver uso ativo, desligue-a; se houver, encerre apenas os serviços do projeto concluído e informe a dependência restante.
- Confira o estado final: nenhum contêiner de teste da tarefa em execução e a VM dedicada marcada como Stopped. Informe o nome do projeto e da VM ao concluir.
- Preserve código, alterações locais, bancos, volumes e evidências únicas. Parar uma VM não autoriza apagar seu disco; não use limpeza geral de volumes. Remova contêineres ou dados somente quando descartáveis e dentro do escopo autorizado.
- Estas regras se limitam aos ambientes locais de teste. Não desligue servidores ou serviços de produção por esta rotina.
