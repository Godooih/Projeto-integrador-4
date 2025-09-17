const { DataTypes } = require("sequelize");
const sequelize = require("../config/database");

const Ativo = sequelize.define("Ativo", {
  nome: { type: DataTypes.STRING, allowNull: false },
  descricao: { type: DataTypes.TEXT },
  tipo: { type: DataTypes.STRING },
  status: { type: DataTypes.STRING, defaultValue: "ativo" },
  data_aquisicao: { type: DataTypes.DATE }
});

module.exports = Ativo;
