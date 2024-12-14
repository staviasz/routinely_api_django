forget_password_template = """<html>
  <head>
    <style>
      * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
      }
      body {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        margin: auto;
        padding: 40px;
        max-width: 1024px;
      }
      header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 80px;
      }
      header > span {
        color: #5c59bb;
        font-family: 'Inter', sans-serif;
      }
      section {
        display: flex;
        flex-direction: column;
        justify-content: center;
        row-gap: 32px;
      }
      #code {
        font-weight: bolder;
        font-size: 44px;
      }
      #sub-title {
        font-size: 24px;
        font-weight: bold;
      }
      footer {
        max-width: 1024px;
        position: relative;
        bottom: 0;
        width: 100%;
      }
      footer > p {
        padding: 16px 0;
        border-top: 1px solid black;
      }
    </style>
  </head>
  <body>
    <div>
      <header>
        <img
          src="https://routnely-assets.vercel.app/logoHorizontalSecondary.svg"
          alt="logo Routnely"
        />
        <span>Redefinir Senha</span>
      </header>
      <section>
        <h2 id="sub-title">Olá, ${name}! precisa alterar a sua senha?</h2>
        <p>Aqui está o código de segurança da sua conta Routinely:</p>
        <h1 id="code"><strong>${code}</strong></h1>
        <p>
          Use o código acima para verificar a propriedade de sua conta. Como
          medida de segurança, o código irá expirar em 15 minutos.
        </p>
        <p>
          Se você não solicitou a alteração de senha, é só ignorar este e-mail.
        </p>
      </section>
    </div>
    <footer>
      <p>© {{year}} Routinely. Todos os direitos reservados.</p>
    </footer>
  </body>
</html>"""
