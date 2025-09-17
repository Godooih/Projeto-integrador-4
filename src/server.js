const express = require("express");
const sequelize = require("./config/database");
const Usuario = require("./models/Usuario");
const Ativo = require("./models/Ativo");
const Chamado = require("./models/Chamado");

const usuariosRoutes = require("./routes/usuarios");
const ativosRoutes = require("./routes/ativos");
const chamadosRoutes = require("./routes/chamados");

const app = express();
app.use(express.json());

// Rotas
app.use("/usuarios", usuariosRoutes);
app.use("/ativos", ativosRoutes);
app.use("/chamados", chamadosRoutes);

// Sincronizar banco e iniciar servidor
sequelize.sync().then(() => {
  app.listen(3000, () => {
    console.log("Servidor rodando em http://localhost:3000");
  });
});
