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
  "planoId" BIGINT,
  dia INTEGER,
  quantidade INTEGER,
  PRIMARY KEY (id),
  CONSTRAINT fk_planoId FOREIGN KEY("planoId") REFERENCES planos (id)
);

CREATE TABLE IF NOT EXISTS confinamentos  (
  id SERIAL NOT NULL,
  "planoId" BIGINT,
  "matrizId" BIGINT,
  dataConfinamento timestamp,
  active BOOLEAN,
  PRIMARY KEY (id),
  CONSTRAINT fk_planoId FOREIGN KEY("planoId") REFERENCES planos (id),
  CONSTRAINT fk_matrizId FOREIGN KEY("matrizId") REFERENCES matrizes (id)
);

CREATE TABLE IF NOT EXISTS  registros  (
  id SERIAL NOT NULL,
  "matrizId" BIGINT,
  dataEntrada timestamp,
  dataSaida timestamp,
  tempo INTEGER,
  quantidade INTEGER,
  PRIMARY KEY (id),
  CONSTRAINT fk_matrizId FOREIGN KEY("matrizId") REFERENCES matrizes (id)
);

CREATE TABLE IF NOT EXISTS  inseminacoes  (
  id SERIAL NOT NULL,
  "planoId" BIGINT,
  "matrizId" BIGINT,
  "confinamentoId" BIGINT,
  dataInseminacao timestamp,
  active BOOLEAN,
  PRIMARY KEY (id),
  CONSTRAINT fk_planoId FOREIGN KEY("planoId") REFERENCES planos (id),
  CONSTRAINT fk_matrizId FOREIGN KEY("matrizId") REFERENCES matrizes (id),
  CONSTRAINT fk_confinamentoId FOREIGN KEY("confinamentoId") REFERENCES confinamentos (id)
);

CREATE TABLE IF NOT EXISTS avisos (
  id SERIAL NOT NULL,
  "confinamentoId" BIGINT,
  dataAviso timestamp,
  separar BOOLEAN,
  status BOOLEAN,
  active BOOLEAN,
  PRIMARY KEY (id),
  CONSTRAINT fk_confinamentoId FOREIGN KEY("confinamentoId") REFERENCES confinamentos (id)
);