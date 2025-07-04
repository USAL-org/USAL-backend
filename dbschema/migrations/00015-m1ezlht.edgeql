CREATE MIGRATION m1ezlhtpn524a7rflawcjjxqkrkglezui2z66xcn6dkfzrfppivjga
    ONTO m13ffnru5qbiyzofybhiwhz33ggtzp75kjzv35jh7jytn6cyfp6n2q
{
  ALTER TYPE default::University {
      ALTER PROPERTY annual_fee {
          SET TYPE std::float64 USING (<std::float64>.annual_fee);
      };
  };
};
