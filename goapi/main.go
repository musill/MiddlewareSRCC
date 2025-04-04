package main

import (
	"go-api/database"
	"go-api/controllers"
	"github.com/gin-gonic/gin"
)

func main() {
	database.Connect()
	r := gin.Default()

	r.POST("/profesor", controllers.CrearProfesor)
	r.POST("/asignatura", controllers.CrearAsignatura)
	r.POST("/profesor_ciclo", controllers.CrearProfesorCiclo)
	r.GET("/ciclos", controllers.ListarCiclos)

	r.Run(":8080")
}
