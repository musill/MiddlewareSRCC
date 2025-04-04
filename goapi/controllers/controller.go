package controllers

import (
	"go-api/database"
	"go-api/models"
	"github.com/gin-gonic/gin"
	"net/http"
)

func CrearProfesor(c *gin.Context) {
	var prof models.Profesor
	if err := c.ShouldBindJSON(&prof); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	database.DB.Create(&prof)
	c.JSON(http.StatusOK, prof)
}

func CrearAsignatura(c *gin.Context) {
	var asignatura models.Asignatura
	if err := c.ShouldBindJSON(&asignatura); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	database.DB.Create(&asignatura)
	c.JSON(http.StatusOK, asignatura)
}

func CrearProfesorCiclo(c *gin.Context) {
	var ciclo models.ProfesorCiclo
	if err := c.ShouldBindJSON(&ciclo); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}
	database.DB.Create(&ciclo)
	c.JSON(http.StatusOK, ciclo)
}

func ListarCiclos(c *gin.Context) {
	var ciclos []models.ProfesorCiclo
	database.DB.Find(&ciclos)
	c.JSON(http.StatusOK, ciclos)
}
