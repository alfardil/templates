# Prerequisties

## Running the server

```bash
just dev
```

### Backend

#### Install [air](https://github.com/air-verse/air) for live-reloading on your Go server.

```bash
go install github.com/air-verse/air@latest
```

Then you can run your server with:

```bash
just go-dev
```

### Frontend

Run the frontend with:

```bash
just js-dev
```

### Database

Run your migration with:

```bash
just migrate up
```

Other possible commands:

```bash
just migrate drop # drop the database
just migrate down # rollback the last applied migration(s)
```
