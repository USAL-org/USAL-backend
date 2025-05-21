CREATE MIGRATION m1bourgyhuxfmxh6ohxg4iobc6zzwxhwb4pawi4unr4wfwg3xizlzq
    ONTO m15t7qyscxhj6ams62da7zp32wjlg7kgpujfvqcpxz642ols55cufa
{
  ALTER TYPE default::State {
      CREATE REQUIRED PROPERTY country: std::str {
          SET REQUIRED USING (<std::str>{});
      };
  };
};
