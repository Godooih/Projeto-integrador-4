const { DataTypes } = require("sequelize");
const sequelize = require("../config/database");
const Usuario = require("./Usuario.js");
const Ativo = require("./Ativo.js");

const Chamado = sequelize.define("Chamado", {
  titulo: { type: DataTypes.STRING, allowNull: false },
  descricao: { type: DataTypes.TEXT },
  prioridade: { type: DataTypes.ENUM("baixa", "media", "alta"), defaultValue: "baixa" },
  status: { type: DataTypes.ENUM("aberto", "em andamento", "resolvido"), defaultValue: "aberto" }
});

Chamado.belongsTo(Usuario, { foreignKey: "usuario_id" });
Chamado.belongsTo(Ativo, { foreignKey: "ativo_id" });

module.exports = Chamado;
