CREATE MIGRATION m1nxk2bhhhhzxb5b7ejmxdnda64mjxuj4dakjsa4bwpuzetbrjlzbq
    ONTO m1ivlhbckdpn3br3kamadapyeerztpcl2qgozpeg62oecuk35b5cha
{
  CREATE SCALAR TYPE default::AdminPermissions EXTENDING enum<ARTICLE_MANAGEMENT, UNIVERSITY_MANAGEMENT, QA_MANAGEMENT, RESOURCES_MANAGEMENT, NOTIFICATION_MANAGEMENT, USER_MANAGEMENT, MARKETING_MANAGEMENT>;
  CREATE SCALAR TYPE default::Gender EXTENDING enum<MALE, FEMALE, OTHERS>;
  CREATE SCALAR TYPE default::UserStatus EXTENDING enum<ACTIVE, INACTIVE, DELETED>;
  ALTER TYPE default::Admin {
      CREATE PROPERTY super_admin: std::bool {
          SET default := false;
      };
  };
  CREATE TYPE default::AdminPermission EXTENDING default::DateTime {
      CREATE REQUIRED LINK admin: default::Admin;
      CREATE REQUIRED MULTI PROPERTY permission: default::AdminPermissions;
  };
  CREATE TYPE default::User EXTENDING default::DateTime {
      CREATE PROPERTY date_of_birth: std::cal::local_date;
      CREATE REQUIRED PROPERTY email: std::str;
      CREATE REQUIRED PROPERTY first_name: std::str;
      CREATE PROPERTY gender: default::Gender;
      CREATE REQUIRED PROPERTY last_name: std::str;
      CREATE PROPERTY middle_name: std::str;
      CREATE REQUIRED PROPERTY password_hash: std::str;
      CREATE REQUIRED PROPERTY phone_number: std::str;
      CREATE PROPERTY pp_url: std::str;
      CREATE REQUIRED PROPERTY status: default::UserStatus {
          SET default := (default::UserStatus.ACTIVE);
      };
      CREATE REQUIRED PROPERTY verified: std::bool {
          SET default := false;
      };
  };
};
