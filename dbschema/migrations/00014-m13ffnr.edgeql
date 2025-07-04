CREATE MIGRATION m13ffnru5qbiyzofybhiwhz33ggtzp75kjzv35jh7jytn6cyfp6n2q
    ONTO m1uu4shfjll5rv5tbocpnta73nylp5ffmso3he3xuc4exssxjahc3q
{
  ALTER TYPE default::University {
      ALTER PROPERTY annual_fee {
          SET TYPE std::str USING (<std::str>.annual_fee);
      };
  };
};
