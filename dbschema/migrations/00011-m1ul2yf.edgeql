CREATE MIGRATION m1ul2yfowvqhkpm3lkiwhnlq5bxjdbz57trn4gbmd7b4wz63mj7jha
    ONTO m1fypbbbrcytnblrof5i66llwth6xqdtffvurtayhkzba2o2glvoaq
{
  ALTER TYPE default::University {
      ALTER PROPERTY annual_fee {
          SET TYPE std::float64 USING (<std::float64>.annual_fee);
      };
  };
};
