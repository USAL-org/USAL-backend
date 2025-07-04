CREATE MIGRATION m1y24uoorbgg3i6i7476bk7xwba63liqt54ivug5xdzx4we4glu3aa
    ONTO m1ul2yfowvqhkpm3lkiwhnlq5bxjdbz57trn4gbmd7b4wz63mj7jha
{
  ALTER TYPE default::University {
      ALTER PROPERTY acceptance_rate {
          SET TYPE std::float64 USING (<std::float64>.acceptance_rate);
      };
  };
};
