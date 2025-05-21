CREATE MIGRATION m15t7qyscxhj6ams62da7zp32wjlg7kgpujfvqcpxz642ols55cufa
    ONTO m17wta2dxiakrf4vwxhpbuabmxrsqjolskwpxlvjrnirmt2w6q2kwa
{
  ALTER TYPE default::University {
      DROP PROPERTY pp_url;
  };
};
