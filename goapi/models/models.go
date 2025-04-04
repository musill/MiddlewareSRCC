package models

import "time"

type Profesor struct {
	ID      uint   `gorm:"primaryKey" json:"id"`
	Cedula  string `json:"cedula"`
	Nombre  string `json:"nombre"`
}

type Asignatura struct {
	ID     uint   `gorm:"primaryKey" json:"id"`
	Nombre string `json:"nombre"`
	Nivel  string `json:"nivel"`
}

type ProfesorCiclo struct {
	ID           uint      `gorm:"primaryKey" json:"id"`
	FechaInicio  time.Time `json:"fecha_inicio"`
	FechaFin     time.Time `json:"fecha_fin"`
	ProfesorID   uint      `json:"profesor_id"`
	AsignaturaID uint      `json:"asignatura_id"`
}
