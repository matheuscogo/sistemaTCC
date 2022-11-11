CREATE TABLE IF NOT EXISTS matrizes  (
  id SERIAL NOT NULL,
  rfid VARCHAR,
  numero VARCHAR,
  ciclos INTEGER,
  deleted BOOLEAN,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS planos  (
  id SERIAL NOT NULL,
  nome VARCHAR,
  descricao VARCHAR,
  tipo VARCHAR,
  quantidadeDias INTEGER,
  deleted BOOLEAN,
  active BOOLEAN,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS dias  (
  id SERIAL NOT NULL,
  plano_id BIGINT,
  dia INTEGER,
  quantidade INTEGER,
  PRIMARY KEY (id),
  CONSTRAINT fk_planoId FOREIGN KEY("plano_id") REFERENCES planos (id)
);

CREATE TABLE IF NOT EXISTS confinamentos  (
  id SERIAL NOT NULL,
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
  id SERIAL NOT NULL,
  matriz_id BIGINT,
  data_entrada timestamp,
  data_saida timestamp,
  tempo INTEGER,
  quantidade INTEGER,
  PRIMARY KEY (id),
  CONSTRAINT fk_matriz_id FOREIGN KEY("matriz_id") REFERENCES matrizes (id)
);

CREATE TABLE IF NOT EXISTS  inseminacoes  (
  id SERIAL NOT NULL,
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
  id SERIAL NOT NULL,
  confinamento_id BIGINT,
  dataAviso timestamp,
  separar BOOLEAN,
  status BOOLEAN,
  active BOOLEAN,
  PRIMARY KEY (id),
  CONSTRAINT fk_confinamento_id FOREIGN KEY("confinamento_id") REFERENCES confinamentos (id)
);