package utils

import (
	"fmt"
	"time"

	"github.com/alfardil/syllendar_go/database/repository/session"
	"github.com/alfardil/syllendar_go/database/repository/user"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type AuthenticationObject struct {
	User    *user.User       `json:"user"`
	Session *session.Session `json:"session"`
}

func ValidateRequest(
	c *gin.Context,
	userRepository user.UserRepository,
	sessionRepository session.SessionRepository,
) (*AuthenticationObject, error) {
	v, err := c.Cookie("session")
	if err != nil {
		return nil, fmt.Errorf("failed to validate request: %w", err)
	}

	uuid, err := uuid.Parse(v)
	if err != nil {
		return nil, fmt.Errorf("invalid session id: %w", err)
	}

	session, err := sessionRepository.GetSessionById(c.Request.Context(), uuid)
	if err != nil {
		return nil, fmt.Errorf("failed to find session with given id: %w", err)
	}

	if time.Now().After(session.ExpiresAt) {
		return nil, fmt.Errorf("session has expired")
	}

	user, err := userRepository.GetUserById(c.Request.Context(), session.UserId)
	if err != nil {
		return nil, fmt.Errorf("failed to find user from session's user id: %w", err)
	}

	return &AuthenticationObject{
		User:    user,
		Session: session,
	}, nil
}
