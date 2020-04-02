DROP TABLE IF EXISTS collab_recommendations CASCADE;

CREATE TABLE  collab_recommendations(
    segment VARCHAR(255),
    target_audience VARCHAR(255),
    product_recommendation VARCHAR(255)[]
);

DROP TABLE IF EXISTS content_recommendations CASCADE;

CREATE TABLE  content_recommendations(
    category VARCHAR(255),
    product_recommendation VARCHAR(255)
);

DROP TABLE IF EXISTS recurring_recommendations CASCADE;

CREATE TABLE  ecurring_recommendations(
    profile_id VARCHAR(255),
    product_id VARCHAR(255),
    average_return_time TIMESTAMP(0),
    amount_bought VARCHAR(255)
);