const express = require("express");
const Usuario = require("../models/Usuario");
const router = express.Router();

// Listar todos
router.get("/", async (req, res) => {
  const usuarios = await Usuario.findAll();
  res.json(usuarios);
});

// Buscar por ID
router.get("/:id", async (req, res) => {
  const usuario = await Usuario.findByPk(req.params.id);
  usuario ? res.json(usuario) : res.status(404).json({ error: "Usuário não encontrado" });
});

// Criar
router.post("/", async (req, res) => {
  const usuario = await Usuario.create(req.body);
  res.status(201).json(usuario);
});

// Atualizar
router.put("/:id", async (req, res) => {
  const usuario = await Usuario.findByPk(req.params.id);
  if (usuario) {
    await usuario.update(req.body);
    res.json(usuario);
  } else {
    res.status(404).json({ error: "Usuário não encontrado" });
  }
});

// Deletar
router.delete("/:id", async (req, res) => {
  const usuario = await Usuario.findByPk(req.params.id);
  if (usuario) {
    await usuario.destroy();
    res.json({ message: "Usuário removido" });
  } else {
    res.status(404).json({ error: "Usuário não encontrado" });
  }
});

module.exports = router;
