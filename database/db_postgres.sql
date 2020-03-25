-- -----------------------------------------------------
-- Table brand
-- -----------------------------------------------------

DROP SEQUENCE IF EXISTS brand_seq CASCADE;
CREATE SEQUENCE brand_seq;

DROP TABLE IF EXISTS brand CASCADE;
CREATE TABLE IF NOT EXISTS brand (
  id INT NULL DEFAULT NEXTVAL ('brand_seq'),
  name VARCHAR(255) NULL,
  PRIMARY KEY (id));

-- -----------------------------------------------------
-- Table products
-- -----------------------------------------------------
DROP TABLE IF EXISTS products CASCADE;

CREATE TABLE IF NOT EXISTS products (
  id VARCHAR(255) NULL,
  brand_id INT NULL,
  name VARCHAR(255) NULL,
  targetaudience VARCHAR(255) NULL,
  category VARCHAR(255) NULL,
  sub_category VARCHAR(255) NULL,
  sub_sub_category VARCHAR(255) NULL,
  msrp VARCHAR(45) NULL,
  discount VARCHAR(45) NULL,
  sellingprice VARCHAR(45) NULL,
  deal VARCHAR(255) NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_products_brand1
    FOREIGN KEY (brand_id)
    REFERENCES brand (id)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table profiles
-- -----------------------------------------------------
DROP TABLE IF EXISTS profiles CASCADE;

CREATE TABLE IF NOT EXISTS profiles (
  id VARCHAR(255) NULL,
  order_amount INT NULL DEFAULT 0,
  latest TIMESTAMP(0) NULL,
  segment VARCHAR(45) NULL,
  PRIMARY KEY (id));


-- -----------------------------------------------------
-- Table sessions
-- -----------------------------------------------------
DROP TABLE IF EXISTS sessions CASCADE;

CREATE TABLE IF NOT EXISTS sessions (
  browser_id VARCHAR(255) NOT NULL,
  profiles_id VARCHAR(255) NULL,
  segment VARCHAR(45) NULL,
  starttime TIMESTAMP(0) NULL,
  endtime TIMESTAMP(0) NULL,
  devicetype VARCHAR(45) NULL);


-- -----------------------------------------------------
-- Table cart
-- -----------------------------------------------------
DROP TABLE IF EXISTS cart CASCADE;

CREATE TABLE IF NOT EXISTS cart (
  products_id VARCHAR(255) NULL,
  sessions_profiles_id VARCHAR(255) NULL,
  bought SMALLINT NULL);