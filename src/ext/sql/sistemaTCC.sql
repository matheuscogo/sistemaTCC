CREATE TABLE IF NOT EXISTS matrizes (
  id BIGINT NOT NULL,
  rfid VARCHAR NULL,
  numero VARCHAR NULL,
  ciclos INTEGER NULL,
  deleted BOOLEAN NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS planos (
  id BIGINT NOT NULL,
  nome VARCHAR NULL,
  descricao VARCHAR NULL,
  tipo VARCHAR NULL,
  quantidadeDias INTEGER NULL,
  deleted BOOLEAN NULL,
  active BOOLEAN NULL,
  PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS confinamentos (
  id BIGINT NOT NULL,
  data_confinamento DATETIME NULL,
  active BOOLEAN NULL,
  deleted BOOLEAN NULL,
  matrizes_id INTEGER NOT NULL,
  planos_id INTEGER NOT NULL,
  matrizes_id1 INTEGER NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_confinamentos_planos1
    FOREIGN KEY (planos_id)
    REFERENCES planos (id),
  CONSTRAINT fk_confinamentos_matrizes1
    FOREIGN KEY (matrizes_id1)
    REFERENCES matrizes (id)
);

CREATE TABLE IF NOT EXISTS dias (
  id BIGINT NOT NULL,
  dia INTEGER NULL,
  quantidade INTEGER NULL,
  planos_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_dias_planos1
    FOREIGN KEY (planos_id)
    REFERENCES planos (id)
);

CREATE TABLE IF NOT EXISTS avisos (
  id BIGINT NOT NULL,
  data_aviso DATETIME NULL,
  separate BOOLEAN NULL,
  tipo INTEGER NULL,
  active BOOLEAN NULL,
  deleted BOOLEAN NULL,
  confinamentos_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_avisos_confinamentos1
    FOREIGN KEY (confinamentos_id)
    REFERENCES confinamentos (id)
);

CREATE TABLE IF NOT EXISTS inseminacoes (
  id BIGINT NOT NULL,
  data_inseminacao DATETIME NULL,
  active BOOLEAN NULL,
  deleted BOOLEAN NULL,
  confinamentos_id INTEGER NOT NULL,
  matrizes_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_inseminacoes_confinamentos1
    FOREIGN KEY (confinamentos_id , matrizes_id)
    REFERENCES confinamentos (id , matrizes_id)
);

CREATE TABLE IF NOT EXISTS alimentador (
  id BIGINT NOT NULL,
  data_entrada DATETIME NULL,
  hash VARCHAR(16) NULL,
  confinamentos_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_alimentador_confinamentos1
    FOREIGN KEY (confinamentos_id)
    REFERENCES confinamentos (id)
);

CREATE TABLE IF NOT EXISTS registros (
  id BIGINT NOT NULL,
  data_entrada DATETIME NULL,
  data_saida DATETIME NULL,
  quantidade INTEGER NULL,
  confinamentos_id INTEGER NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_Registros_matrizes1
    FOREIGN KEY (matrizes_id)
    REFERENCES matrizes (id)
);

CREATE TABLE IF NOT EXISTS alimentador  (
  id INTEGER NOT NULL,
  matriz_id INTEGER,
  confinamento_id INTEGER,
  plano_id INTEGER,
  dataEntrada DATETIME,
  quantidade INTEGER,
  hash VARCHAR,
  PRIMARY KEY (id),
  FOREIGN KEY(matriz_id) REFERENCES matrizes (id),
  FOREIGN KEY(confinamento_id) REFERENCES confinamentos (id),
  FOREIGN KEY(plano_id) REFERENCES planos (id)
);

CREATE TABLE parametros  (
  id INTEGER NOT NULL,
  tempoPorção INTEGER NOT NULL,
  quantidadePorção INTEGER NOT NULL,
  intervaloPorções INTEGER NOT NULL,
  tempoProximaMatriz INTEGER NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO parametros VALUES (1, 30, 500, 30, 60)