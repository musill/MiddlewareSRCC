package database

import (
	"fmt"
	"log"
	"os"

	"github.com/joho/godotenv"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"

	"go-api/models" 
)

var DB *gorm.DB

func Connect() {
	// Cargar variables del archivo .env
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error al cargar el archivo .env:", err)
	}

	// Obtener variables de entorno
	host := os.Getenv("MYSQL_HOST")
	user := os.Getenv("MYSQL_USER")
	password := os.Getenv("MYSQL_PASSWORD")
	dbname := os.Getenv("MYSQL_DB")

	// Crear el DSN dinámicamente
	dsn := fmt.Sprintf("%s:%s@tcp(%s:3306)/%s?charset=utf8mb4&parseTime=True&loc=Local",
		user, password, host, dbname)

	// Conexión con GORM
	database, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
	if err != nil {
		log.Fatal("Error al conectar a MySQL:", err)
	}

	// Migraciones
	database.AutoMigrate(&models.Profesor{}, &models.Asignatura{}, &models.ProfesorCiclo{})
	DB = database
}
