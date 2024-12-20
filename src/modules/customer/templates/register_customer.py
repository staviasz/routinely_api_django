from main.utils import template_to_strings


register_customer_template = """<html>
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
        font-family: "Inter", sans-serif;
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
      #title {
        font-size: 24px;
        font-weight: bold;
      }
      button {
        max-width: 140px;
        background-color: #5c59bb;
        color: white;
        border: none;
        border-radius: 8px;
        cursor: pointer;
      }
      section > button {
        margin-bottom: 62px;
      }

      #container-img {
        display: flex;
        flex-direction: column;
        align-items: end;
      }
      #container-img > img {
        max-width: 700px;
        width: 100%;
      }
      button > a {
        display: block;
        text-decoration: none;
        color: white;
        font-weight: bold;
        padding: 12px 16px;
      }
      footer {
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
          alt="logo Routinely"
        />
        <span>Criação de Conta Routinely</span>
      </header>
      <section>
        <h1 id="title">Seja Bem vindo(a) ao Routinely!</h1>
        <p>
          Sua conta foi criada com sucesso! Para ativá-la, confirme o seu login
          de e-mail no botão abaixo.
        </p>
        <button type="button">
          <a href="${url}" target="_blank">Vamos começar</a>
        </button>
        <div id="container-img">
          <img
            src="https://routnely-assets.vercel.app/signInPageImage.svg"
            alt=""
          />
        </div>
      </section>
    </div>
    <footer>
      <p>© ${year} Routinely. Todos os direitos reservados.</p>
    </footer>
  </body>
</html>"""
