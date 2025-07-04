CREATE MIGRATION m1uu4shfjll5rv5tbocpnta73nylp5ffmso3he3xuc4exssxjahc3q
    ONTO m1y24uoorbgg3i6i7476bk7xwba63liqt54ivug5xdzx4we4glu3aa
{
  ALTER TYPE default::University {
      CREATE PROPERTY min_gpa: std::float64 {
          SET default := 0;
      };
      CREATE REQUIRED PROPERTY test_required: std::bool {
          SET default := false;
      };
  };
};
