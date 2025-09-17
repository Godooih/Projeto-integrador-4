const express = require("express");
const Ativo = require("../models/Ativo");
const router = express.Router();

// Listar todos
router.get("/", async (req, res) => {
  const ativo = await Ativo.findAll();
  res.json(ativo);
});

// Buscar por ID
router.get("/:id", async (req, res) => {
  const ativo = await Ativo.findByPk(req.params.id);
  ativo ? res.json(ativo) : res.status(404).json({ error: "Ativo não encontrado" });
});

// Criar
router.post("/", async (req, res) => {
  const ativo = await Ativo.create(req.body);
  res.status(201).json(ativo);
});

// Atualizar
router.put("/:id", async (req, res) => {
  const ativo = await Ativo.findByPk(req.params.id);
  if (ativo) {
    await ativo.update(req.body);
    res.json(ativo);
  } else {
    res.status(404).json({ error: "Ativo não encontrado" });
  }
});

// Deletar
router.delete("/:id", async (req, res) => {
  const ativo = await Ativo.findByPk(req.params.id);
  if (ativo) {
    await ativo.destroy();
    res.json({ message: "Ativo removido" });
  } else {
    res.status(404).json({ error: "Ativo não encontrado" });
  }
});

module.exports = router;
