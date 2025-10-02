package api

import (
	"net/http"

	"github.com/alfardil/syllendar_go/api/auth"
	"github.com/alfardil/syllendar_go/database/repository/session"
	"github.com/alfardil/syllendar_go/database/repository/user"
	"github.com/gin-gonic/gin"
	"github.com/jackc/pgx/v5/pgxpool"
)

func NewRouter(eng *gin.Engine, db *pgxpool.Pool) *gin.RouterGroup {
	r := eng.Group("/api")

	r.GET("", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "Testing!",
		})
	})

	userRepository := user.NewPostgresUserRepository(db)
	sessionRepository := session.NewPostgresSessionRepository(db)
	auth.NewRouter(r, userRepository, sessionRepository)

	return r
}
