package api

import (
	"log"

	"github.com/alfardil/syllendar_go/database"
	"github.com/alfardil/syllendar_go/database/repository/session"
	"github.com/alfardil/syllendar_go/database/repository/user"
	"github.com/jackc/pgx/v5/pgxpool"
)

type AppContext struct {
	Db                *pgxpool.Pool
	UserRepository    *user.PostgresUserRepository
	SessionRepository *session.PostgresSessionRepository
}

func (c *AppContext) databaseBuilder() {
	if c.Db == nil {
		err := database.Connect()
		if err != nil {
			log.Fatalf("Failed to connect to database: %v", err)
		}

		db, err := database.GetPool()
		if err != nil {
			log.Fatalf("Failed to get database pool: %v", err)
		}
		c.Db = db
	}
}

func (c *AppContext) repositoryBuilder() {
	if c.UserRepository == nil {
		c.UserRepository = user.NewPostgresUserRepository(c.Db)
	}
	if c.SessionRepository == nil {
		c.SessionRepository = session.NewPostgresSessionRepository(c.Db)
	}
}
