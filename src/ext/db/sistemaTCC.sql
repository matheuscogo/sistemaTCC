CREATE TABLE IF NOT EXISTS matrizes  (
  id INTEGER,
  rfid VARCHAR,
  numero VARCHAR,
  ciclos INTEGER,
  deleted BOOLEAN,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS planos  (
  id INTEGER,
  nome VARCHAR,
  descricao VARCHAR,
  tipo VARCHAR,
  quantidadeDias INTEGER,
  deleted BOOLEAN,
  active BOOLEAN,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS dias  (
  id INTEGER,
  plano_id BIGINT,
  dia INTEGER,
  quantidade INTEGER,
  PRIMARY KEY (id),
  CONSTRAINT fk_planoId FOREIGN KEY("plano_id") REFERENCES planos (id)
);

CREATE TABLE IF NOT EXISTS confinamentos  (
  id INTEGER,
  plano_id BIGINT,
  matriz_id BIGINT,
  data_confinamento timestamp,
  active BOOLEAN,
  deleted BOOLEAN,
  PRIMARY KEY (id),
  CONSTRAINT fk_planoId FOREIGN KEY("plano_id") REFERENCES planos (id),
  CONSTRAINT fk_matriz_id FOREIGN KEY("matriz_id") REFERENCES matrizes (id)
);

CREATE TABLE IF NOT EXISTS  registros  (
  id INTEGER,
  matriz_id BIGINT,
  data_entrada timestamp,
  data_saida timestamp,
  quantidade INTEGER,
  PRIMARY KEY (id),
  CONSTRAINT fk_matriz_id FOREIGN KEY("matriz_id") REFERENCES matrizes (id)
);

CREATE TABLE IF NOT EXISTS  inseminacoes  (
  id INTEGER,
  plano_id BIGINT,
  matriz_id BIGINT,
  confinamento_id BIGINT,
  data_inseminacao timestamp,
  active BOOLEAN,
  deleted BOOLEAN,
  PRIMARY KEY (id),
  CONSTRAINT fk_planoId FOREIGN KEY("plano_id") REFERENCES planos (id),
  CONSTRAINT fk_matriz_id FOREIGN KEY("matriz_id") REFERENCES matrizes (id),
  CONSTRAINT fk_confinamento_id FOREIGN KEY("confinamento_id") REFERENCES confinamentos (id)
);

CREATE TABLE IF NOT EXISTS avisos (
  id INTEGER,
  confinamento_id BIGINT NULL,
  data_aviso timestamp,
  separate BOOLEAN,
  type INTEGER,
  active BOOLEAN,
  deleted BOOLEAN,
  PRIMARY KEY (id),
  CONSTRAINT fk_confinamento_id FOREIGN KEY("confinamento_id") REFERENCES confinamentos (id)
);