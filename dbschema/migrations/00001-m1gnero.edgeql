CREATE MIGRATION m1gneroa67coilsqbknpo43tnjk7dpkkczo43rmzntoxisi5jmo4nq
    ONTO initial
{
  CREATE SCALAR TYPE default::ArticleStatus EXTENDING enum<ACTIVE, INACTIVE>;
  CREATE SCALAR TYPE default::ArticleType EXTENDING enum<NEWS, BLOG>;
  CREATE SCALAR TYPE default::QAStatus EXTENDING enum<ACTIVE, INACTIVE>;
  CREATE SCALAR TYPE default::QAType EXTENDING enum<UNIVERSITY, ACADEMIC, FINANCIAL, PERSONAL, GRADUATE, POST_GRADUATE, PHD, FAMILY>;
  CREATE SCALAR TYPE default::ResourceStatus EXTENDING enum<ACTIVE, INACTIVE>;
  CREATE SCALAR TYPE default::UniversityStatus EXTENDING enum<ACTIVE, INACTIVE>;
  CREATE FUTURE simple_scoping;
  CREATE ABSTRACT TYPE default::DateTime {
      CREATE REQUIRED PROPERTY created_at: std::datetime {
          SET default := (std::datetime_current());
      };
      CREATE REQUIRED PROPERTY updated_at: std::datetime {
          SET default := (std::datetime_current());
      };
  };
  CREATE TYPE default::Admin EXTENDING default::DateTime {
      CREATE REQUIRED PROPERTY email: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
      CREATE REQUIRED PROPERTY password_hash: std::str;
      CREATE PROPERTY pp_url: std::str;
      CREATE REQUIRED PROPERTY username: std::str {
          CREATE CONSTRAINT std::exclusive;
      };
  };
  CREATE TYPE default::ArticleCategory EXTENDING default::DateTime {
      CREATE REQUIRED PROPERTY name: std::str;
  };
  CREATE TYPE default::Author EXTENDING default::DateTime {
      CREATE PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY email: std::str;
      CREATE REQUIRED PROPERTY full_name: std::str;
      CREATE PROPERTY pp_url: std::str;
      CREATE REQUIRED PROPERTY short_description: std::str;
      CREATE MULTI PROPERTY social_links: std::str;
  };
  CREATE TYPE default::Article EXTENDING default::DateTime {
      CREATE REQUIRED LINK author: default::Author;
      CREATE REQUIRED LINK category: default::ArticleCategory;
      CREATE REQUIRED PROPERTY content: std::str;
      CREATE REQUIRED PROPERTY cover_image: std::str;
      CREATE MULTI PROPERTY media: std::str;
      CREATE REQUIRED PROPERTY status: default::ArticleStatus {
          SET default := (default::ArticleStatus.ACTIVE);
      };
      CREATE PROPERTY time_elascate: std::str;
      CREATE REQUIRED PROPERTY title: std::str;
      CREATE REQUIRED PROPERTY type: default::ArticleType {
          SET default := (default::ArticleType.BLOG);
      };
  };
  CREATE TYPE default::Major EXTENDING default::DateTime {
      CREATE PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
  };
  CREATE TYPE default::QASection EXTENDING default::DateTime {
      CREATE REQUIRED PROPERTY answer: std::str;
      CREATE REQUIRED PROPERTY question: std::str;
      CREATE REQUIRED PROPERTY status: default::QAStatus {
          SET default := (default::QAStatus.ACTIVE);
      };
      CREATE REQUIRED PROPERTY type: default::QAType {
          SET default := (default::QAType.UNIVERSITY);
      };
  };
  CREATE TYPE default::Resources EXTENDING default::DateTime {
      CREATE REQUIRED PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY file: std::str;
      CREATE REQUIRED PROPERTY image: std::str;
      CREATE REQUIRED PROPERTY status: default::ResourceStatus {
          SET default := (default::ResourceStatus.ACTIVE);
      };
      CREATE REQUIRED PROPERTY title: std::str;
  };
  CREATE TYPE default::State EXTENDING default::DateTime {
      CREATE REQUIRED PROPERTY name: std::str;
  };
  CREATE TYPE default::University EXTENDING default::DateTime {
      CREATE MULTI LINK available_majors: default::Major;
      CREATE REQUIRED LINK state: default::State;
      CREATE REQUIRED PROPERTY acceptance_rate: std::str;
      CREATE REQUIRED MULTI PROPERTY admission_requirements: std::str;
      CREATE REQUIRED PROPERTY annual_fee: std::str;
      CREATE PROPERTY application_fee: std::bool;
      CREATE PROPERTY community_college: std::bool;
      CREATE PROPERTY description: std::str;
      CREATE REQUIRED PROPERTY image: std::str;
      CREATE REQUIRED PROPERTY location: std::str;
      CREATE REQUIRED PROPERTY name: std::str;
      CREATE PROPERTY pp_url: std::str;
      CREATE REQUIRED PROPERTY status: default::UniversityStatus {
          SET default := (default::UniversityStatus.ACTIVE);
      };
      CREATE PROPERTY student_faculty_ratio: std::str;
      CREATE PROPERTY view_count: std::int32 {
          SET default := 0;
      };
  };
};
