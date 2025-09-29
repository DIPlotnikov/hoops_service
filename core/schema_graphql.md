{
  "data": {
    "__schema": {
      "types": [
        {
          "name": "Query",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "adminFilterExecutorByWhatever",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "phonenumberCheckExists",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminPaymentPing",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "managerGetAllBlackList",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerGetMyTask",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerGetAllTaskForAdmin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerGetExecutersByTaskid",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "managerGetTaskById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerGetTasksByMonth",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "managerGetTasksByDate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "executerAllTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerTask",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerMyTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "executerGetTaskAtTheMoment",
              "type": {
                "name": "TaskType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "executerGetTaskById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerMyStatusOfTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "executerGetCountAllTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executerGetIdAndDateAllExecuterStatesByMonth",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "executerGetExecuterStateById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "adminGetTasksByHotelId",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskForAdminTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetTaskById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskForAdminType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminAllTask",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskForAdminTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "tasksHotelById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerGetMyReport",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "executerGetMyReport",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "adminGetReports",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "managerGetMyFeedback",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "executerGetMyFeedback",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "feedbackGetAboutExecuter",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "feedbackGetAboutCustomer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "statistics",
              "type": {
                "name": "StatisticType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "executerAddress",
              "type": {
                "name": "AddressType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "executerPassport",
              "type": {
                "name": "PassportDataType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "getReadNotifications",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "NotifyTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "getUnreadNotifications",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "getCountUnreadNotifications",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "getAllNotifications",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "NotifyTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "allGetPostsLanding",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostLandingTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetPostsLanding",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostLandingTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "allGetPostLandingByUrl",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostLandingType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "allLogo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "adminGetLogo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "adminGetLogoById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "LogoType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "allGetPosts",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetPosts",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetNoticeByFilters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "NoticeTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetNoticeById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "NoticeType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerGetNoticeByFilters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "NoticeTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerGetNoticeById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "NoticeType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetClosingDocumentsByFilters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ClosingDocumentTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetClosingDocumentById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ClosingDocumentType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerGetClosingDocumentById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ClosingDocumentType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerGetClosingDocumentsByFilters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ClosingDocumentTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "allGetMainOffer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AgreementType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "allGetActualAgreementByType",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AgreementType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "allGetAgreementsTypes",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "allGetAllOffers",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "allGetAllAgreements",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "managerGetPersonalProfessions",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PersonalProfessionsBlockType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "allGetInfoBlocks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "adminGetInfoBlocks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "InfoBlockTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "allGetCategoryInfoBlocks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "validateToken",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ValidateTokenType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executers",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerMe",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerPermints",
              "type": {
                "name": "ExecuterPermintsType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "executerCheckCodeByPhone",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executerGetFavoriteHotels",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "profession",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ProfessionType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "professions",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "professionGetCost",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminGetExecuterNotices",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterNoticeTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetExecuterNoticeById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterNoticeType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerGetExecuterNotices",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "executerRequisites",
              "type": {
                "name": "RequisitesType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "executerGetSimpleRequisite",
              "type": {
                "name": "SimpleRequisiteType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerBool",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "managerMe",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerGetMyManagers",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "managerGetRequisitesOfMyHotel",
              "type": {
                "name": "RequisitesType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "managerGetFavoriteExecuters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "hotelById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerGetCustomerLocationList",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "executerGetCustomerById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminMe",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminAllAdmins",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetAdminsByName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "adminFilterAdminByWhatever",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "adminAllHotels",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "hotelForAdminConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminAllManagers",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "managerForAdminConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetHotelById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "hotelForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminFilterHotelByWhatever",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "adminAllExecuters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdminConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetExecuterById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetPaymentsOfExecuterById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PaymentJumpFinanceTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminCheckExecuterInFns",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminGetCurrentTaskIdExecuter",
              "type": {
                "name": "TaskForAdminType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "adminPaymentGetAll",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PaymentTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminPaymentGetByHotelId",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PaymentTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminPaymentGetById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PaymentType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminPaymentGetAllIndividual",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PaymentTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetTasksByStatus",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskForAdminTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetTaskPaymentExecutersByStatus",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskForAdminTypeConnection",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "executerForAdmin",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "lastLogin",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "profilePic",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "firstName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "secondName",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "middleName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "birthday",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Date",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "gender",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsExecuterGenderChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "workExpiration",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "medicalBookExpiration",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "phoneNumber",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "email",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "StatusExecuter",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "professions",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "kind",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsExecuterKindChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "other",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "about",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isTest",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "agreementDatetime",
              "type": {
                "name": "Date",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "updatePasswordAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "executernoticeSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "score",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "countWorkWithRating",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isValidNumber",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isActive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "createdAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updatedAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "simplerequisite",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SimpleRequisiteType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "countDayForLastTask",
              "type": {
                "name": "Int",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "countDayForEndRegistration",
              "type": {
                "name": "Int",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "countDayForEndMedicalBook",
              "type": {
                "name": "Int",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "inn",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "passportData",
              "type": {
                "name": "PassportDataType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "address",
              "type": {
                "name": "AddressType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "isAdminCanSendPush",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "jumpFinance",
              "type": {
                "name": "JumpFinanceContractor",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "citizenship",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "notice",
              "type": {
                "name": "ExecuterNoticeType",
                "kind": "OBJECT",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "Node",
          "kind": "INTERFACE",
          "description": "An object with an ID",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "ID",
          "kind": "SCALAR",
          "description": "The `ID` scalar type represents a unique identifier, often used to refetch an object or as key for a cache. The ID type appears in a JSON response as a String; however, it is not intended to be human-readable. When expected as an input type, any string (such as `\"4\"`) or integer (such as `4`) input value will be accepted as an ID.",
          "fields": null
        },
        {
          "name": "DateTime",
          "kind": "SCALAR",
          "description": "The `DateTime` scalar type represents a DateTime\nvalue as specified by\n[iso8601](https://en.wikipedia.org/wiki/ISO_8601).",
          "fields": null
        },
        {
          "name": "FileInfoType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "fileName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "fileSize",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "height",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "width",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "mimeType",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "timeStamp",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "url",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "String",
          "kind": "SCALAR",
          "description": "The `String` scalar type represents textual data, represented as UTF-8 character sequences. The String type is most often used by GraphQL to represent free-form human-readable text.",
          "fields": null
        },
        {
          "name": "Int",
          "kind": "SCALAR",
          "description": "The `Int` scalar type represents non-fractional signed whole numeric values. Int can represent values between -(2^31) and 2^31 - 1.",
          "fields": null
        },
        {
          "name": "Date",
          "kind": "SCALAR",
          "description": "The `Date` scalar type represents a Date\nvalue as specified by\n[iso8601](https://en.wikipedia.org/wiki/ISO_8601).",
          "fields": null
        },
        {
          "name": "HotelsExecuterGenderChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "StatusExecuter",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "ProfessionType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "description",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "rateMax",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "rateMin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "rateStep",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "percent",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "numerate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsProfessionNumerateChoices",
                  "kind": "ENUM"
                }
              }
            }
          ]
        },
        {
          "name": "HotelsProfessionNumerateChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "HotelsExecuterKindChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "Boolean",
          "kind": "SCALAR",
          "description": "The `Boolean` scalar type represents `true` or `false`.",
          "fields": null
        },
        {
          "name": "ExecuterNoticeType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "admin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "files",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "createAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isAutoGenerate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "adminForAdmin",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "lastLogin",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isActive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "role",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "surname",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "firstName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "middleName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "percent",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminstatdocSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "postlandingSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostLandingTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "permissions",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsAdminPermissionsChoices",
                  "kind": "ENUM"
                }
              }
            }
          ]
        },
        {
          "name": "Float",
          "kind": "SCALAR",
          "description": "The `Float` scalar type represents signed double-precision fractional values as specified by [IEEE 754](https://en.wikipedia.org/wiki/IEEE_floating_point).",
          "fields": null
        },
        {
          "name": "AdminReportDocType",
          "kind": "OBJECT",
          "description": "Отчёт Администратора",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "type",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TypeAdminReport",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "dateUpdate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "TypeAdminReport",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "PostLandingTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "PageInfo",
          "kind": "OBJECT",
          "description": "The Relay compliant `PageInfo` type, containing data necessary to paginate this connection.",
          "fields": [
            {
              "name": "hasNextPage",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "hasPreviousPage",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "startCursor",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "endCursor",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "PostLandingTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `PostLandingType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostLandingType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "PostLandingType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "admin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "title",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "content",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "hashtag",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "url",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isPublic",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "createAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updateAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "files",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "HotelsAdminPermissionsChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "ExecuterType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "lastLogin",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "profilePic",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "firstName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "secondName",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "middleName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "birthday",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "gender",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsExecuterGenderChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "workExpiration",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "medicalBookExpiration",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "phoneNumber",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "email",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsExecuterStatusChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "professions",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "kind",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsExecuterKindChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "other",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "about",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isTest",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "agreementDatetime",
              "type": {
                "name": "Date",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "updatePasswordAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "executernoticeSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterNoticeTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "inn",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "rating",
              "type": {
                "name": "Float",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "favoriteHotels",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "isFavorite",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isBlacklist",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "HotelsExecuterStatusChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "ExecuterNoticeTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "ExecuterNoticeTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `ExecuterNoticeType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterNoticeType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "SimpleRequisiteType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "inn",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "cardNumber",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "PassportDataType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "citizenship",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "EnumCitizenShip",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "citizenshipOther",
              "type": {
                "name": "CitizenshipOther",
                "kind": "ENUM",
                "ofType": null
              }
            },
            {
              "name": "series",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "number",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "issuedBy",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "dateOfIssue",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "subdivisionCode",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "placeBirth",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "passportData",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "EnumCitizenShip",
          "kind": "ENUM",
          "description": null,
          "fields": null
        },
        {
          "name": "CitizenshipOther",
          "kind": "ENUM",
          "description": "Тип гражданства",
          "fields": null
        },
        {
          "name": "AddressType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "coordinates",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CoordinatesExecuterType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "CoordinatesExecuterType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "latitude",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "longitude",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "address",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "label",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "JumpFinanceContractor",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "idContractor",
              "type": {
                "name": "Int",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "isVerified",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isCanPayTaxes",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "hasCompanyAgreesPayTaxes",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "hasWarning",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "lastMessage",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "createAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updateAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "FilterExecutorInput",
          "kind": "INPUT_OBJECT",
          "description": "Инпут для фильтрации исполнителей",
          "fields": null
        },
        {
          "name": "PhonenumberInput",
          "kind": "INPUT_OBJECT",
          "description": "Инпут для номера телефона",
          "fields": null
        },
        {
          "name": "Phonenumber",
          "kind": "SCALAR",
          "description": "номер телефона: 11 цифр, формат 79xxxxxxxxx",
          "fields": null
        },
        {
          "name": "ExecuterTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "ExecuterTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `ExecuterType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "TaskTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "TaskTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `TaskType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "TaskType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "profession",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ProfessionType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "personalProfession",
              "type": {
                "name": "PersonalProfessionType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "countExecuters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "rent",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "startAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "duration",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "comment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executers",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "minRating",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsTaskStatusChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "forFavorite",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isApproved",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isArchived",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "additional",
              "type": {
                "name": "AdditionalTaskType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "createdAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updatedAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "startAtDate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Date",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "startAtTime",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Time",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isClosed",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "commentOfTask",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "approvedStatus",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ApprovedStatus",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "countExecutorsWithStart",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "countExecutorsWithStop",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "countExecutorsViolators",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "ManagerType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "lastLogin",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "email",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "firstName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "secondName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "middleName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "isAdmin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isActive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Status",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "updatePasswordAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "admin",
              "type": {
                "name": "adminForAdmin",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "roles",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "statdocSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "countTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "favoriteExecuters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "blacklistExecuters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "HotelType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "email",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "inn",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "postalAddress",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "nameLegalEntity",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "nameHotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "undergroundStation",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "phoneNumber",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "profilePic",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "logo",
              "type": {
                "name": "LogoType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "coordinates",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CoordinatesType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsHotelStatusChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "autoApproveTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isAllowToUseBasicProfession",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isActive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isVerify",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isTest",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "fcmToken",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "maxCountOfPersonalProfession",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "paymentPeriodToHoops",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsHotelPaymentPeriodToHoopsChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "paymentPeriodToExecutor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsHotelPaymentPeriodToExecutorChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "mayUseAdditionalInTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "acceptedAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "createdAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updatedAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executerSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdminConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "personalprofessionSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "noticeSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "NoticeTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "countTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "rating",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "LogoType",
          "kind": "OBJECT",
          "description": "Логотип",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "description",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "isVisible",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "createAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updateAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "hotel",
              "type": {
                "name": "hotelForAdmin",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "files",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "hotelForAdmin",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "email",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "inn",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "postalAddress",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "nameLegalEntity",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "nameHotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "undergroundStation",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "phoneNumber",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "profilePic",
              "type": {
                "name": "FileInfoType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "logo",
              "type": {
                "name": "LogoType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "coordinates",
              "type": {
                "name": "CoordinatesType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsHotelStatusChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "autoApproveTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isAllowToUseBasicProfession",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isActive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isVerify",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isTest",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "fcmToken",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "maxCountOfPersonalProfession",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "paymentPeriodToHoops",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsHotelPaymentPeriodToHoopsChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "paymentPeriodToExecutor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsHotelPaymentPeriodToExecutorChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "mayUseAdditionalInTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "acceptedAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "createdAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updatedAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executerSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdminConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "personalprofessionSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "noticeSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "NoticeTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "requisites",
              "type": {
                "name": "RequisitesType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "managerSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "rating",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "mainManagerFullName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "CoordinatesType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "latitude",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "longitude",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "address",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "label",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "HotelsHotelStatusChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "HotelsHotelPaymentPeriodToHoopsChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "HotelsHotelPaymentPeriodToExecutorChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "executerForAdminConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "executerForAdminEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `executerForAdmin` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "PersonalProfessionType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "analog",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ProfessionType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "rent",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "active",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "forExecuter",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "NoticeTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "NoticeTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `NoticeType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "NoticeType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "NoticeType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "admin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "hotelForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "files",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "subject",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isArchive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isSent",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "createAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "RequisitesType",
          "kind": "OBJECT",
          "description": "Реквизиты Гостиницы",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "paymentBill",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "correctBill",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "kpp",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "innBank",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "bik",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "ogrn",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "legalAddress",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "signer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "Status",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "RolesManager",
          "kind": "ENUM",
          "description": "Роли менеджера",
          "fields": null
        },
        {
          "name": "ReportDocType",
          "kind": "OBJECT",
          "description": "Отчёт менеджера",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "type",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TypeReportDoc",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "dateUpdate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "TypeReportDoc",
          "kind": "ENUM",
          "description": null,
          "fields": null
        },
        {
          "name": "ExecuterStateType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsExecuterStateStatusChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "startAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "stopAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "volumeOfTheWork",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "correctionComment",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "paymentStatus",
              "type": {
                "name": "PaymentStatus",
                "kind": "ENUM",
                "ofType": null
              }
            },
            {
              "name": "payment",
              "type": {
                "name": "PaymentType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "feedback",
              "type": {
                "name": "FeedbackAboutExecuterByManagerType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "isViolator",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isTest",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "payInRubles",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "HotelsExecuterStateStatusChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "PaymentStatus",
          "kind": "ENUM",
          "description": null,
          "fields": null
        },
        {
          "name": "PaymentType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "admin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "type",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PaymentEnum",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "startDate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "endDate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "statusExecuters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsPaymentStatusExecutersChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "filePathExecuter",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "createAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updateAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "logData",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "isBusy",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isArchive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isIndividual",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executerstateSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "hotelForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "receipts",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "canDelete",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "sumForPayWithTax",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "sumPaid",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "countSentReceipts",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "tasksId",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "PaymentEnum",
          "kind": "ENUM",
          "description": null,
          "fields": null
        },
        {
          "name": "HotelsPaymentStatusExecutersChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "ExecuterStateTypeForAdmin",
          "kind": "OBJECT",
          "description": "Статус отклика исполнителя для Админа",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsExecuterStateStatusChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "startAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "stopAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "volumeOfTheWork",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "correctionComment",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "paymentStatus",
              "type": {
                "name": "PaymentStatus",
                "kind": "ENUM",
                "ofType": null
              }
            },
            {
              "name": "payment",
              "type": {
                "name": "PaymentType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "feedback",
              "type": {
                "name": "FeedbackAboutExecuterByManagerType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "isViolator",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isTest",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "payInRubles",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "FeedbackAboutExecuterByManagerType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskForAdminType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "rating",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "comment",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "createdAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updatedAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "TaskForAdminType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "profession",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ProfessionType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "personalProfession",
              "type": {
                "name": "PersonalProfessionType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "countExecuters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "rent",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "startAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "duration",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "comment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executers",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "minRating",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsTaskStatusChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "forFavorite",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isApproved",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isArchived",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "additional",
              "type": {
                "name": "AdditionalTaskType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "createdAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updatedAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "personalProfessionName",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "paymentStatus",
              "type": {
                "name": "PaymentStatus",
                "kind": "ENUM",
                "ofType": null
              }
            },
            {
              "name": "isArchivedForAdmin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "closingdocumentSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ClosingDocumentTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "commentoftaskSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "paymentSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PaymentTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "paymentStatusForExecuter",
              "type": {
                "name": "PaymentStatus",
                "kind": "ENUM",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "HotelsTaskStatusChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "AdditionalTaskType",
          "kind": "OBJECT",
          "description": "Тип дополнительной информации по Заявке",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "datetime",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "description",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "ClosingDocumentTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "ClosingDocumentTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `ClosingDocumentType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ClosingDocumentType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "ClosingDocumentType",
          "kind": "OBJECT",
          "description": "Тип Закрывающих документов",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "admin",
              "type": {
                "name": "adminForAdmin",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "tasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskForAdminTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "files",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "startDate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "endDate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "createAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isArchive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isPaid",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isSent",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isBlock",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "closingDatetime",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "TaskForAdminTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "TaskForAdminTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `TaskForAdminType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskForAdminType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "DocumentFileType",
          "kind": "OBJECT",
          "description": "Файл закрывающих документов",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "number",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "amount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "closingdocumentSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ClosingDocumentTypeConnection",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "CommentOfTaskType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "text",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "createdAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updatedAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "PaymentTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "PaymentTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `PaymentType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PaymentType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "PaymentJumpFinanceType",
          "kind": "OBJECT",
          "description": "Выплата JumpFinance",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "idPayment",
              "type": {
                "name": "Int",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "amount",
              "type": {
                "name": "Float",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "amountPaid",
              "type": {
                "name": "Float",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "comission",
              "type": {
                "name": "Float",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "comissionBank",
              "type": {
                "name": "Float",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "taxAmount",
              "type": {
                "name": "Float",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "purpose",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsPaymentJumpFinanceStatusChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "fnsKey",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "fnsUrl",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "savedUrl",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "isFinal",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "createAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updateAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "HotelsPaymentJumpFinanceStatusChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "Time",
          "kind": "SCALAR",
          "description": "The `Time` scalar type represents a Time value as\nspecified by\n[iso8601](https://en.wikipedia.org/wiki/ISO_8601).",
          "fields": null
        },
        {
          "name": "ApprovedStatus",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "inputForGetMyTasks",
          "kind": "INPUT_OBJECT",
          "description": "Инпут для получения совиз Заявок",
          "fields": null
        },
        {
          "name": "inputId",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputDateTime",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "inputForGetTasks",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "Sort",
          "kind": "ENUM",
          "description": null,
          "fields": null
        },
        {
          "name": "SortFields",
          "kind": "ENUM",
          "description": null,
          "fields": null
        },
        {
          "name": "ExecuterTaskType",
          "kind": "OBJECT",
          "description": "Task for executer",
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "feedback",
              "type": {
                "name": "FeedbackAboutTaskByExecuterType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterStateType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "FeedbackAboutTaskByExecuterType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskForAdminType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "rating",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "comment",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "createdAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updatedAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "ExecuterStateTypeForExecuter",
          "kind": "OBJECT",
          "description": "Статус отклика исполнителя для Исполнителя",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsExecuterStateStatusChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "startAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "stopAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "volumeOfTheWork",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "correctionComment",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "paymentStatus",
              "type": {
                "name": "PaymentStatus",
                "kind": "ENUM",
                "ofType": null
              }
            },
            {
              "name": "payment",
              "type": {
                "name": "PaymentType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "feedback",
              "type": {
                "name": "FeedbackAboutExecuterByManagerType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "isViolator",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isTest",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "payInRubles",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "ExecuterStateIDAndTAskStartAt",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "startAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputIDs",
          "kind": "INPUT_OBJECT",
          "description": "Входной параметр список ID",
          "fields": null
        },
        {
          "name": "InputForAllTaskForAdmin",
          "kind": "INPUT_OBJECT",
          "description": "Фильтры заявок для таблицы Администратора",
          "fields": null
        },
        {
          "name": "ExecuterReportDocType",
          "kind": "OBJECT",
          "description": "Отчёт исполнителя",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "type",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TypeExecutersDoc",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "dateUpdate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "TypeExecutersDoc",
          "kind": "ENUM",
          "description": null,
          "fields": null
        },
        {
          "name": "InputFeedbackAbout",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "StatisticType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executers",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "customers",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "tasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "executersInWork",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "NotifyTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "NotifyTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `NotifyType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "NotifyType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "NotifyType",
          "kind": "OBJECT",
          "description": "Уведомление",
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "type",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsNotificationTypeChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "idInstance",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "text",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "createdAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "read",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "meta",
              "type": {
                "name": "MetaType",
                "kind": "OBJECT",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "HotelsNotificationTypeChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "MetaType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "taskId",
              "type": {
                "name": "Int",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "InputForQueryNotification",
          "kind": "INPUT_OBJECT",
          "description": "Параметры получения Уведомлений",
          "fields": null
        },
        {
          "name": "TypeNotification",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "InputForQueryPostLandingWithFilters",
          "kind": "INPUT_OBJECT",
          "description": "Фильтры для отображения постов на лендинге",
          "fields": null
        },
        {
          "name": "InputURL",
          "kind": "INPUT_OBJECT",
          "description": "Входной параметр URL",
          "fields": null
        },
        {
          "name": "InputID",
          "kind": "INPUT_OBJECT",
          "description": "Входной параметр ID",
          "fields": null
        },
        {
          "name": "PostTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "PostTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `PostType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "PostType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "admin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "title",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "content",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "visible",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TypeVisible",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "isPublic",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "createAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updateAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "files",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "TypeVisible",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "InputForQueryPostWithFilters",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputForQueryNotices",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputForQueryNotice",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputForManagerQueryNotices",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputForQueryClosingDocuments",
          "kind": "INPUT_OBJECT",
          "description": "Параметры запроса таблицы закрывающих документов для Гостиниц",
          "fields": null
        },
        {
          "name": "InputForQueryClosingDocument",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputForManagerQueryClosingDocuments",
          "kind": "INPUT_OBJECT",
          "description": "Параметры запроса закрывающих документов для Менеджера",
          "fields": null
        },
        {
          "name": "AgreementType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "type",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TypeAgreement",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "isActual",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "file",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "FileInfoType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "createAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "TypeAgreement",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "InputTypeAgreement",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "PersonalProfessionsBlockType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "personalProfession",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "maxCountOfPersonalProfessions",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InfoBlockType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "category",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "title",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "content",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "files",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "weight",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "visible",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TypeVisible",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "isPublic",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "createAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "updateAt",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InfoBlockTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InfoBlockTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `InfoBlockType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "InfoBlockType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputForQueryInfoBlocksWithFilters",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "ValidateTokenType",
          "kind": "OBJECT",
          "description": "Информация из токена доступа",
          "fields": [
            {
              "name": "type",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "meta",
              "type": {
                "name": "MetaInformationType",
                "kind": "OBJECT",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "MetaInformationType",
          "kind": "OBJECT",
          "description": "Мета информация из токена",
          "fields": [
            {
              "name": "permissions",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "InputForValidateToken",
          "kind": "INPUT_OBJECT",
          "description": "Входные параметры валидации токена",
          "fields": null
        },
        {
          "name": "ExecuterPermintsType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "workExpiration",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "medicalBookExpiration",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DateTime",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "executerInputValidatePhone",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "HotelTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "HotelTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `HotelType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputForGetCost",
          "kind": "INPUT_OBJECT",
          "description": "Параметры запроса стоимости часа по профессии",
          "fields": null
        },
        {
          "name": "InputForQueryExecuterNotices",
          "kind": "INPUT_OBJECT",
          "description": "Параметры запроса таблицы уведомлений для Исполнителей",
          "fields": null
        },
        {
          "name": "inputForQueryById",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "adminType",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "lastLogin",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isActive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "role",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "surname",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "firstName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "middleName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "percent",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Float",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminstatdocSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "postlandingSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostLandingTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "roles",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "Roles",
          "kind": "ENUM",
          "description": "Роли Администратора",
          "fields": null
        },
        {
          "name": "adminTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "adminTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `adminType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputName",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "FilterAdminInput",
          "kind": "INPUT_OBJECT",
          "description": "Инпут для фильтрации админов",
          "fields": null
        },
        {
          "name": "hotelForAdminConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "hotelForAdminEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `hotelForAdmin` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "hotelForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputForQueryAllHotels",
          "kind": "INPUT_OBJECT",
          "description": "Инпут запроса всех гостиниц",
          "fields": null
        },
        {
          "name": "Statuses",
          "kind": "ENUM",
          "description": "Статусы Гостиниц",
          "fields": null
        },
        {
          "name": "managerForAdminConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "managerForAdminEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `managerForAdmin` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "managerForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "managerForAdmin",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "id",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ID",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "lastLogin",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "email",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "firstName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "secondName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "middleName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "hotelForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "isAdmin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "isActive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "status",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelsManagerStatusChoices",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "updatePasswordAt",
              "type": {
                "name": "DateTime",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "favouriteExecuters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdminConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "admin",
              "type": {
                "name": "adminForAdmin",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "statdocSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "taskSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskForAdminTypeConnection",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "feedbackmanagerSet",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "HotelsManagerStatusChoices",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "inputEmailAndInn",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputINN",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputNameHotel",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputNameOrInn",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputForFilterHotels",
          "kind": "INPUT_OBJECT",
          "description": "Фильтрация Гостиниц",
          "fields": null
        },
        {
          "name": "InputForQueryAllExecuter",
          "kind": "INPUT_OBJECT",
          "description": "ИНпут запроса списка Исполнителей",
          "fields": null
        },
        {
          "name": "InputForGetExecuterByName",
          "kind": "INPUT_OBJECT",
          "description": "Параметры поиска Исполнителя по имени",
          "fields": null
        },
        {
          "name": "PaymentJumpFinanceTypeConnection",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "pageInfo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PageInfo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "edges",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "totalCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "edgeCount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Int",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "PaymentJumpFinanceTypeEdge",
          "kind": "OBJECT",
          "description": "A Relay edge containing a `PaymentJumpFinanceType` and its cursor.",
          "fields": [
            {
              "name": "node",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PaymentJumpFinanceType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "cursor",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputArchive",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputIdAndArchive",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputId",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputPaymentForAdmin",
          "kind": "INPUT_OBJECT",
          "description": "Фильтры для Выплат",
          "fields": null
        },
        {
          "name": "inputPaymentStatus",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "Mutation",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "managerExecutorAddInBlackListById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "managerExecutorRemoveFromBlackListById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "managerExecutorFlushAllBlackList",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminCreateClosingDocumentByIdHotelAndStartEndDate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreateClosingDocument",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminArchiveClosingDocuments",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ArchiveClosingDocuments",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminActivateClosingDocuments",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ActivateClosingDocuments",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminSendClosingDocuments",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SendClosingDocuments",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminMarkAsPaidClosingDocuments",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "MarAsPaidClosingDocuments",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminBlockPeriodClosingDocumentsById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "BlockPeriodClosingDocuments",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUpsertAgreement",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AdminUpsertAgreement",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerUpsertFeedbackAboutTask",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpsertFeedbackExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerUpsertFeedbackAboutExecuterInTask",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpsertFeedbackManager",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerTaskRequest",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "requestTask",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerRequestTaskDelete",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "deleteRequestTask",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerTaskUpsert",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpsertTask",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerTaskDelete",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "deleteTask",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerSetCorrectionCommentToExecuterInTask",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "setCorrectionCommentToExecuterInTask",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerStartTask",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "startTask",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerStopTask",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "stopTask",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerSetVolumeOfWorkByExecuterState",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SetVolumeOfWorkByExecuterState",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerTaskArchive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "archiveTask",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerTaskUnarchive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "unarchiveTask",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerSetExecuterAsViolatorInTaskById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "setExecuterAsViolator",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerSetExecuterAsTester",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TestWork",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerApproveTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ApproveTask",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerForbidTasksWithComment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ForbidTask",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerCreateReport",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreateStat",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerCreateListExecutersTaskById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreateListExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerCreateReport",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreateStatForExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminCreateReportByPeriodAndType",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AdminCreateReport",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUpsertPostLanding",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpsertPostLanding",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminPublishPostLanding",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PublishPostLanding",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUnpublishPostLanding",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UnpublishPostLanding",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminDeletePostLanding",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DeletePostLanding",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUpsertInfoBlock",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpsertInfoBlock",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminPublishInfoBlock",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PublishInfoBlock",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUnpublishInfoBlock",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UnpublishInfoBlock",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminDeleteInfoBlock",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DeleteInfoBlock",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerSetAddress",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerSetAddress",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerUpsertSimpleRequisite",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterUpsertSimpleRequisite",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerUpsertRequisites",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerUpsertRequisites",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerUpsertPassport",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterUpsertPassport",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerDeletePassport",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterDeletePassport",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUploadMedia",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AdminUploadMedia",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminPaymentCreateByPeriod",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreatePayment",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminPaymentCreateByExecuterStateAsIndividualPayment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreatePaymentIndividual",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminPaymentMarkAsPaidToExecuters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "MarkPaymentAsPaidToExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminPaymentArchive",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ArchivePayments",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminPaymentActivate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ActivatePayments",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUpsertJumpfinancePaymentsByIdPayment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpsertPaymentJumpFinance",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUpsertJumpfinancePaymentsByIdPaymentAsync",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminGetDocumentWithJumpfinancePaymentsByIdPayment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreateDocumentPaymentJumpFinance",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminDeletePaymentById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminConfirmHotelPayment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ConfirmHotelPayment",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminDenyHotelPayment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "denyUserPayment",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminMarkHotelAsTestByListOfId",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "MarkHotelsAsTest",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminSetSettingsByHotelId",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SetSettingsHotel",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminConfirmExecuterPayment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "confirmExecuterPayment",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminDenyExecuterPayment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "denyExecuterPayment",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminDeactivateExecutorById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DeactivateExecutor",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminSetPasswordForExecuterById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SetPasswordGorExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminSendPushForExecuterDeviceByListOfIdExecuter",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminMarkExecutersAsTestByListOfId",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "MarkExecutersAsTest",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminSetAgreementDatetimeForExecuter",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SetAgreementDatetimeForExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminCreateDocumentWithExecutorsByFilters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreateBlankWithExecutors",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminSendPushToExecutorsByFilters",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminExecuterSyncJumpFinanceById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SyncJumpFinanceStatus",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminAuthenticate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AuthenticateAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUpsertAdmin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpsertAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminSetFullName",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SetFullNameAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminDeactivate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DeactivateAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminSetNewPasswordForAdminById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SetNewPasswordAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminGetAccessByRoleAndId",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TokenExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerUpdate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpdateManager",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerUpdateRolesManagerById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerType",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerCreateNewManager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "managerCancelInvite",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CancelInvate",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerResendInvite",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ResendInvate",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerAddFavoriteExecuter",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AddFavoriteExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerRemoveFavoriteExecuter",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "RemoveFavoriteExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerClearFavoriteExecuter",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ClearFavoriteExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerDeactivateManager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DeleteManager",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerActivate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ActivateManager",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerDeleteAccount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DeleteAccountManager",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerRequestRecoveryPasswordByInnEmail",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "RequestToRecoveryPasswordByInnEmail",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerRecoveryPasswordByInnEmail",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "RecoveryPasswordByInnEmail",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerSetNewPassword",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SetNewPasswordManager",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerAuthenticateByEmail",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AuthenticateByEmail",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerAuthenticateByInn",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AuthenticateByInn",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerCreateHotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelCreate",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerUpdateHotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelUpdate",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerUploadMedia",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelUploadMedia",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerCreatePayment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelCreatePayment",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerValidateRequisites",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelVerificationRequest",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerChangeAutoApproveTasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelChangeAutoApproveTasks",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerChangeAllowToUseBasicProfessions",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelChangeAllowToUseBasicProfession",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminCreateExecuterStateByTaskIdAndExecuterId",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreateExecuterStateByTaskIDAndExecuterID",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminDeleteExecuterStatesById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminMoveTasksToOneMonthAhead",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "MoveTasksToOneMonthAhead",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminArchiveTasksByIds",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskArchiveForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUnarchiveTasksByIds",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskUnarchiveForAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUpsertLogo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpsertLogo",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminDeleteLogo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminManagerAddAdmin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AddManagerToAdmin",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminManagerClearAdmin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ClearAdminOfManger",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminSetPasswordForManager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SetManagerPassword",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminCreateExecuterNoticeByIdExecuter",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreateExecuterNotice",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminDeleteExecuterNoticeById",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "adminUpsertPost",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpsertPost",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminPublishPost",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PublishPost",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminUnpublishPost",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UnpublishPost",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminDeletePost",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DeletePost",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminCreateNoticeByIdHotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreateNotice",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminArchiveNotice",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ArchiveNotice",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminActivateNotice",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ActivateNotice",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminSendNotice",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SendNotice",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerAuthenticate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AuthenticateExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerCreate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "CreateExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerUpdate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpdateExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerUpdateAvatar",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpdateAvatarExecuter",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerSendCode",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerSendCode",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerUploadMedia",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerUploadMedia",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerCreatePayment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerCreatePayment",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerConfirmBankPaymentByOrderId",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterConfirmBankPaymentByOrderID",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerUpsertPermints",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerUpsertPermints",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerAddFavoriteHotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AddFavoriteHotel",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerRemoveFavoriteHotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "RemoveFavoriteHotel",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerClearFavoriteHotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ClearFavoriteHotel",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerSetNewPassword",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SetNewPassword",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerRequestToDeleteAccount",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "RequestDeleteExecutorAccount",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerDeleteAccountWithCode",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "DeleteAccountExecuterWithCode",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerRequestToRecoveryPasswordByPhone",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "RequestRecoveryPassword",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "executerRecoveryPasswordByPhoneAndCode",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "RecoveryPassword",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "adminProfessionUpsert",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "UpsertProfession",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "notificationRead",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ReadNotify",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerPersonalProfessionCreate",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "createPersonalProfession",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "managerPersonalProfessionDelete",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "deletePersonalProfession",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "CreateClosingDocument",
          "kind": "OBJECT",
          "description": "Создание закрывающих документов Администратором",
          "fields": [
            {
              "name": "closingDocument",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ClosingDocumentType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForCreateClosingDocuments",
          "kind": "INPUT_OBJECT",
          "description": "Создание закрывающих документов",
          "fields": null
        },
        {
          "name": "ArchiveClosingDocuments",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "closingDocuments",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "InputIds",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "ActivateClosingDocuments",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "closingDocuments",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "SendClosingDocuments",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "closingDocuments",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "MarAsPaidClosingDocuments",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "closingDocuments",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "BlockPeriodClosingDocuments",
          "kind": "OBJECT",
          "description": "Блокировка периода на перенос заявок",
          "fields": [
            {
              "name": "closingDocuments",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "AdminUpsertAgreement",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "agreement",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AgreementType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputAgreement",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "fileInfoInput",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "UpsertFeedbackExecuter",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "feedbackExecuter",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "FeedbackAboutTaskByExecuterType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputFeedback",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "UpsertFeedbackManager",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "feedbackManager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "FeedbackAboutExecuterByManagerType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputFeedbackManager",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "requestTask",
          "kind": "OBJECT",
          "description": "Мутация отклика на Заявку",
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "deleteRequestTask",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "UpsertTask",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputForTaskUpsert",
          "kind": "INPUT_OBJECT",
          "description": "Параметры создания и обновления Заявки",
          "fields": null
        },
        {
          "name": "InputForAdditionalTask",
          "kind": "INPUT_OBJECT",
          "description": "Параметры на добавление дополнительной информации к заявке",
          "fields": null
        },
        {
          "name": "deleteTask",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "setCorrectionCommentToExecuterInTask",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputTaskIdExecuterIDCorrection",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "startTask",
          "kind": "OBJECT",
          "description": "Мутация старта Заявки",
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputForStartTask",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "stopTask",
          "kind": "OBJECT",
          "description": "Мутация стопа Заявки",
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputForStopTask",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "SetVolumeOfWorkByExecuterState",
          "kind": "OBJECT",
          "description": "Установка объема выполненных работ по id Отклика Исполнителя",
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForSetVolumeOfWorkInTask",
          "kind": "INPUT_OBJECT",
          "description": "Установка выполненного объема работ по Отклику Исполнителя",
          "fields": null
        },
        {
          "name": "archiveTask",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "tasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "inputIDs",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "unarchiveTask",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "tasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "setExecuterAsViolator",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputTaskIdExecuterID",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "TestWork",
          "kind": "OBJECT",
          "description": "Мутация отметки тестовой работы в Заявке",
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "ApproveTask",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "tasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "ForbidTask",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "tasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "InputForForbidTasks",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "CreateStat",
          "kind": "OBJECT",
          "description": "Создание отчёта для Менеджера",
          "fields": [
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputForStatisticDoc",
          "kind": "INPUT_OBJECT",
          "description": "Параметры генерации отчёта для менеджера",
          "fields": null
        },
        {
          "name": "CreateListExecuter",
          "kind": "OBJECT",
          "description": "Создание списка исполнителей",
          "fields": [
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "inputForListExecuter",
          "kind": "INPUT_OBJECT",
          "description": "Параметры генерации списка исполнителей",
          "fields": null
        },
        {
          "name": "CreateStatForExecuter",
          "kind": "OBJECT",
          "description": "Создание отчёта для исполнителя",
          "fields": [
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputForStatisticDocForExecuter",
          "kind": "INPUT_OBJECT",
          "description": "Параметры генерации отчёта для исполнителя",
          "fields": null
        },
        {
          "name": "AdminCreateReport",
          "kind": "OBJECT",
          "description": "Создание отчёта для Администратора",
          "fields": [
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputForAdminCreateReport",
          "kind": "INPUT_OBJECT",
          "description": "Параметры генерации отчёта для администратора",
          "fields": null
        },
        {
          "name": "UpsertPostLanding",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "post",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostLandingType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForUpsertPostLanding",
          "kind": "INPUT_OBJECT",
          "description": "Создание и обновление поста для лендинга",
          "fields": null
        },
        {
          "name": "PublishPostLanding",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "post",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostLandingType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "UnpublishPostLanding",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "post",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostLandingType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "DeletePostLanding",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "UpsertInfoBlock",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "infoBlock",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "InfoBlockType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForUpsertInfoBlock",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "PublishInfoBlock",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "infoBlock",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "InfoBlockType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "UnpublishInfoBlock",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "infoBlock",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "InfoBlockType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "DeleteInfoBlock",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "executerSetAddress",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "coordinates",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "AddressType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "addressInput",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "coordinatesInput",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "ExecuterUpsertSimpleRequisite",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "requisite",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "SimpleRequisiteType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "SimpleRequisiteInput",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "INN",
          "kind": "SCALAR",
          "description": "ИНН: 12 цифр",
          "fields": null
        },
        {
          "name": "CardNumber",
          "kind": "SCALAR",
          "description": null,
          "fields": null
        },
        {
          "name": "ManagerUpsertRequisites",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "requisites",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "RequisitesType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "requisitesInput",
          "kind": "INPUT_OBJECT",
          "description": "Игпут для создания/обновления реквизитов Гостиницы",
          "fields": null
        },
        {
          "name": "PaymentBill",
          "kind": "SCALAR",
          "description": "Расчетный счет: 20 цифр",
          "fields": null
        },
        {
          "name": "CorrectBill",
          "kind": "SCALAR",
          "description": "Кор счет: 20 цифр",
          "fields": null
        },
        {
          "name": "KPP",
          "kind": "SCALAR",
          "description": "КПП: 9 цифр",
          "fields": null
        },
        {
          "name": "BIK",
          "kind": "SCALAR",
          "description": "БИК: 9 цифр",
          "fields": null
        },
        {
          "name": "ExecuterUpsertPassport",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "passportData",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PassportDataType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputPassportData",
          "kind": "INPUT_OBJECT",
          "description": "Параметры создания паспортных данных",
          "fields": null
        },
        {
          "name": "PassportSeries",
          "kind": "SCALAR",
          "description": null,
          "fields": null
        },
        {
          "name": "SubdivisionCode",
          "kind": "SCALAR",
          "description": null,
          "fields": null
        },
        {
          "name": "ExecuterDeletePassport",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "AdminUploadMedia",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "url",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputTypeMedia",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "TypeDocument",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "CreatePayment",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "payment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PaymentType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputCreatePayments",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "CreatePaymentIndividual",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "payment",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PaymentType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputCreatePaymentIndividual",
          "kind": "INPUT_OBJECT",
          "description": "Параметры создания платежки по идентификатору заявки и исполнителя",
          "fields": null
        },
        {
          "name": "MarkPaymentAsPaidToExecuter",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "payments",
              "type": {
                "name": null,
                "kind": "LIST",
                "ofType": {
                  "name": null,
                  "kind": "NON_NULL"
                }
              }
            }
          ]
        },
        {
          "name": "ArchivePayments",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "payments",
              "type": {
                "name": null,
                "kind": "LIST",
                "ofType": {
                  "name": null,
                  "kind": "NON_NULL"
                }
              }
            }
          ]
        },
        {
          "name": "ActivatePayments",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "payments",
              "type": {
                "name": null,
                "kind": "LIST",
                "ofType": {
                  "name": null,
                  "kind": "NON_NULL"
                }
              }
            }
          ]
        },
        {
          "name": "UpsertPaymentJumpFinance",
          "kind": "OBJECT",
          "description": "Создание или обновление выплат в ЛК JumpFinance",
          "fields": [
            {
              "name": "receipts",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "CreateDocumentPaymentJumpFinance",
          "kind": "OBJECT",
          "description": "Создание или обновление документа с чеками",
          "fields": [
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputForCreatePaymentReport",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "ConfirmHotelPayment",
          "kind": "OBJECT",
          "description": "Подтверждение платежа Гостиницы",
          "fields": [
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "hotelForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputIdDatetime",
          "kind": "INPUT_OBJECT",
          "description": "Инпут для устновки даты и времени по айди",
          "fields": null
        },
        {
          "name": "denyUserPayment",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "hotelForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "MarkHotelsAsTest",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "hotels",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "InputForMarkObjectsAsTest",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "SetSettingsHotel",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "hotelForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForSetSettingsHotel",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "PaymentPeriodToHoops",
          "kind": "ENUM",
          "description": "Период оплаты Гостиниц",
          "fields": null
        },
        {
          "name": "PaymentPeriodToExecutor",
          "kind": "ENUM",
          "description": "Период выплат Исполнителям",
          "fields": null
        },
        {
          "name": "confirmExecuterPayment",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "denyExecuterPayment",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputForDenyExecuterPayment",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "DeactivateExecutor",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "SetPasswordGorExecuter",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputIdPassword",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputForSendPush",
          "kind": "INPUT_OBJECT",
          "description": "Инпут отправки push уведомлений",
          "fields": null
        },
        {
          "name": "MarkExecutersAsTest",
          "kind": "OBJECT",
          "description": "Отметка Исполнителей тестовыми/обычными Админситратором",
          "fields": [
            {
              "name": "executers",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "SetAgreementDatetimeForExecuter",
          "kind": "OBJECT",
          "description": "Установка Даты подписания договора у Исполнителей",
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForSetAgreementDatetime",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "CreateBlankWithExecutors",
          "kind": "OBJECT",
          "description": "Создание или обновление документа с списком Исполнителей",
          "fields": [
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputForSendPushToExecutorsWithFilter",
          "kind": "INPUT_OBJECT",
          "description": "ИНпут для отправки Push уведомления Исполнителям по фильтрам",
          "fields": null
        },
        {
          "name": "SyncJumpFinanceStatus",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "executerForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "AuthenticateAdmin",
          "kind": "OBJECT",
          "description": "Авторизация Администратора",
          "fields": [
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "sessionid",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "adminInputForAuth",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "UpsertAdmin",
          "kind": "OBJECT",
          "description": "Обновление/создание Администратора",
          "fields": [
            {
              "name": "admin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForUpsertAdmin",
          "kind": "INPUT_OBJECT",
          "description": "Инпут для создания/обновления Администратора",
          "fields": null
        },
        {
          "name": "SetFullNameAdmin",
          "kind": "OBJECT",
          "description": "Указание полного имени Администратора",
          "fields": [
            {
              "name": "admin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputFullName",
          "kind": "INPUT_OBJECT",
          "description": "Инпут для изменения полного имени",
          "fields": null
        },
        {
          "name": "DeactivateAdmin",
          "kind": "OBJECT",
          "description": "Деактивация Администратора",
          "fields": [
            {
              "name": "admin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "SetNewPasswordAdmin",
          "kind": "OBJECT",
          "description": "Смена пароля Администратора",
          "fields": [
            {
              "name": "admin",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "adminType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputPassword",
          "kind": "INPUT_OBJECT",
          "description": "Параметры смены пароля",
          "fields": null
        },
        {
          "name": "TokenExecuter",
          "kind": "OBJECT",
          "description": "Получение токена Администратором на вход в профиль",
          "fields": [
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "inputForAcess",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "Objects",
          "kind": "ENUM",
          "description": null,
          "fields": null
        },
        {
          "name": "UpdateManager",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "manager",
              "type": {
                "name": "ManagerType",
                "kind": "OBJECT",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "managerInputForUpdate",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputForUpdateManagerRoles",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "InputForCreateManager",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "Email",
          "kind": "SCALAR",
          "description": null,
          "fields": null
        },
        {
          "name": "CancelInvate",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputEmail",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "ResendInvate",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "metka",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "AddFavoriteExecuter",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputExecuterID",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "RemoveFavoriteExecuter",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "ClearFavoriteExecuter",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "DeleteManager",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "ActivateManager",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "managerInputForActivate",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "DeleteAccountManager",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "RequestToRecoveryPasswordByInnEmail",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "inputInnEmail",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "RecoveryPasswordByInnEmail",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "inputInnEmailSecret",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "SetNewPasswordManager",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ManagerType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputSetNewPasswordManager",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "AuthenticateByEmail",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "inputEmailPassword",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "AuthenticateByInn",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "inputInnPassword",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "HotelCreate",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "inputForCreateHotel",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "HotelUpdate",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputForUpdateHotel",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "HotelUploadMedia",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "url",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "inputForUploadFile",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "HotelCreatePayment",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "HotelVerificationRequest",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "HotelChangeAutoApproveTasks",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "HotelChangeAllowToUseBasicProfession",
          "kind": "OBJECT",
          "description": "Мутация изменения флага использования базовых профессий в заявках",
          "fields": [
            {
              "name": "hotel",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "HotelType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "CreateExecuterStateByTaskIDAndExecuterID",
          "kind": "OBJECT",
          "description": "Создание отклика Администратором",
          "fields": [
            {
              "name": "task",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "TaskForAdminType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputIdTaskIdExecuter",
          "kind": "INPUT_OBJECT",
          "description": "Инпут для устновки отклика",
          "fields": null
        },
        {
          "name": "MoveTasksToOneMonthAhead",
          "kind": "OBJECT",
          "description": "Перемещение откликов на 1 месяц назад",
          "fields": [
            {
              "name": "tasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "TaskArchiveForAdmin",
          "kind": "OBJECT",
          "description": "Переместить в Архив Администратора заявки",
          "fields": [
            {
              "name": "tasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "TaskUnarchiveForAdmin",
          "kind": "OBJECT",
          "description": "Переместить из Архива Администратора заявки",
          "fields": [
            {
              "name": "tasks",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "UpsertLogo",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "logo",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "LogoType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForUpsertLogo",
          "kind": "INPUT_OBJECT",
          "description": "Параметры для создания или обновления логотипа",
          "fields": null
        },
        {
          "name": "AddManagerToAdmin",
          "kind": "OBJECT",
          "description": "Добавление Куратора(Администратора) Менеджеру",
          "fields": [
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "managerForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputManagerIDAdminID",
          "kind": "INPUT_OBJECT",
          "description": "Инпут идентификаторов менеджера и админа",
          "fields": null
        },
        {
          "name": "ClearAdminOfManger",
          "kind": "OBJECT",
          "description": "Очищение Куратора(Администратора) у Менеджера",
          "fields": [
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "managerForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "SetManagerPassword",
          "kind": "OBJECT",
          "description": "Смена пароля у менеджера",
          "fields": [
            {
              "name": "manager",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "managerForAdmin",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "CreateExecuterNotice",
          "kind": "OBJECT",
          "description": "Создание уведомелния для Исполнителя",
          "fields": [
            {
              "name": "executerNotice",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterNoticeType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForCreateExecuterNotice",
          "kind": "INPUT_OBJECT",
          "description": "Параметры создания уведомления для Исполнителя",
          "fields": null
        },
        {
          "name": "UpsertPost",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "post",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForUpsertPost",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "PublishPost",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "post",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "UnpublishPost",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "post",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PostType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "DeletePost",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "CreateNotice",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "notice",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "NoticeType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForCreateNotice",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "ArchiveNotice",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "notices",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "InputIdsNotices",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "ActivateNotice",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "notices",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "SendNotice",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "notices",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "AuthenticateExecuter",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "sessionid",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "inputPhonenumberPassword",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "CreateExecuter",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "executerInputForCreate",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "GenderExecuter",
          "kind": "ENUM",
          "description": "An enumeration.",
          "fields": null
        },
        {
          "name": "UpdateExecuter",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": "ExecuterType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "ok",
              "type": {
                "name": "Boolean",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "executerInputForUpdate",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "UpdateAvatarExecuter",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": "ExecuterType",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "ok",
              "type": {
                "name": "Boolean",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "InputAvatar",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "executerSendCode",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputForSendCode",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "executerUploadMedia",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "url",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "path",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "executerInputFileInfo",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "TypeMedia",
          "kind": "ENUM",
          "description": null,
          "fields": null
        },
        {
          "name": "executerCreatePayment",
          "kind": "OBJECT",
          "description": "Проведение акцепта офферты Исполнителем",
          "fields": [
            {
              "name": "url",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "CreatePaymentInput",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "ExecuterConfirmBankPaymentByOrderID",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "executerUpsertPermints",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "permints",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterPermintsType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputPermints",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "AddFavoriteHotel",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputIDHotel",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "RemoveFavoriteHotel",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "ClearFavoriteHotel",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "SetNewPassword",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "executer",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ExecuterType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "inputSetNewPassword",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "RequestDeleteExecutorAccount",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "DeleteAccountExecuterWithCode",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputCode",
          "kind": "INPUT_OBJECT",
          "description": "Входной параметр секретного кода",
          "fields": null
        },
        {
          "name": "RequestRecoveryPassword",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "RecoveryPassword",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "token",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "InputForRecoveryPassword",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "UpsertProfession",
          "kind": "OBJECT",
          "description": "Обновление/создание профессии Администратором",
          "fields": [
            {
              "name": "profession",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "ProfessionType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "InputForUpsertProfession",
          "kind": "INPUT_OBJECT",
          "description": "Параметры создания/обновления профессии",
          "fields": null
        },
        {
          "name": "Numerates",
          "kind": "ENUM",
          "description": "Тип счисления",
          "fields": null
        },
        {
          "name": "ReadNotify",
          "kind": "OBJECT",
          "description": "Мутация прочтения уведомелний",
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "createPersonalProfession",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "personalProfession",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "PersonalProfessionType",
                  "kind": "OBJECT"
                }
              }
            }
          ]
        },
        {
          "name": "personalProfessionInput",
          "kind": "INPUT_OBJECT",
          "description": null,
          "fields": null
        },
        {
          "name": "deletePersonalProfession",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "ok",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            }
          ]
        },
        {
          "name": "Subscription",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "managerNotificationCreate",
              "type": {
                "name": "MySubscription",
                "kind": "OBJECT",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "MySubscription",
          "kind": "OBJECT",
          "description": null,
          "fields": [
            {
              "name": "text",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "__Schema",
          "kind": "OBJECT",
          "description": "A GraphQL Schema defines the capabilities of a GraphQL server. It exposes all available types and directives on the server, as well as the entry points for query, mutation, and subscription operations.",
          "fields": [
            {
              "name": "description",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "types",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "queryType",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "__Type",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "mutationType",
              "type": {
                "name": "__Type",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "subscriptionType",
              "type": {
                "name": "__Type",
                "kind": "OBJECT",
                "ofType": null
              }
            },
            {
              "name": "directives",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "__Type",
          "kind": "OBJECT",
          "description": "The fundamental unit of any GraphQL Schema is the type. There are many kinds of types in GraphQL as represented by the `__TypeKind` enum.\n\nDepending on the kind of a type, certain fields describe information about that type. Scalar types provide no information beyond a name, description and optional `specifiedByURL`, while Enum types provide their values. Object and Interface types provide the fields they describe. Abstract types, Union and Interface, provide the Object types possible at runtime. List and NonNull types compose other types.",
          "fields": [
            {
              "name": "kind",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "__TypeKind",
                  "kind": "ENUM"
                }
              }
            },
            {
              "name": "name",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "description",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "specifiedByURL",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "fields",
              "type": {
                "name": null,
                "kind": "LIST",
                "ofType": {
                  "name": null,
                  "kind": "NON_NULL"
                }
              }
            },
            {
              "name": "interfaces",
              "type": {
                "name": null,
                "kind": "LIST",
                "ofType": {
                  "name": null,
                  "kind": "NON_NULL"
                }
              }
            },
            {
              "name": "possibleTypes",
              "type": {
                "name": null,
                "kind": "LIST",
                "ofType": {
                  "name": null,
                  "kind": "NON_NULL"
                }
              }
            },
            {
              "name": "enumValues",
              "type": {
                "name": null,
                "kind": "LIST",
                "ofType": {
                  "name": null,
                  "kind": "NON_NULL"
                }
              }
            },
            {
              "name": "inputFields",
              "type": {
                "name": null,
                "kind": "LIST",
                "ofType": {
                  "name": null,
                  "kind": "NON_NULL"
                }
              }
            },
            {
              "name": "ofType",
              "type": {
                "name": "__Type",
                "kind": "OBJECT",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "__TypeKind",
          "kind": "ENUM",
          "description": "An enum describing what kind of type a given `__Type` is.",
          "fields": null
        },
        {
          "name": "__Field",
          "kind": "OBJECT",
          "description": "Object and Interface types are described by a list of Fields, each of which has a name, potentially a list of arguments, and a return type.",
          "fields": [
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "description",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "args",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "type",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "__Type",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "isDeprecated",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "deprecationReason",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "__InputValue",
          "kind": "OBJECT",
          "description": "Arguments provided to Fields or Directives and the input fields of an InputObject are represented as Input Values which describe their type and optionally a default value.",
          "fields": [
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "description",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "type",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "__Type",
                  "kind": "OBJECT"
                }
              }
            },
            {
              "name": "defaultValue",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "isDeprecated",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "deprecationReason",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "__EnumValue",
          "kind": "OBJECT",
          "description": "One possible value for a given Enum. Enum values are unique values, not a placeholder for a string or numeric value. However an Enum value is returned in a JSON response as a string.",
          "fields": [
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "description",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "isDeprecated",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "deprecationReason",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            }
          ]
        },
        {
          "name": "__Directive",
          "kind": "OBJECT",
          "description": "A Directive provides a way to describe alternate runtime execution and type validation behavior in a GraphQL document.\n\nIn some cases, you need to provide options to alter GraphQL's execution behavior in ways field arguments will not suffice, such as conditionally including or skipping a field. Directives provide this by describing additional information to the executor.",
          "fields": [
            {
              "name": "name",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "String",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "description",
              "type": {
                "name": "String",
                "kind": "SCALAR",
                "ofType": null
              }
            },
            {
              "name": "isRepeatable",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": "Boolean",
                  "kind": "SCALAR"
                }
              }
            },
            {
              "name": "locations",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            },
            {
              "name": "args",
              "type": {
                "name": null,
                "kind": "NON_NULL",
                "ofType": {
                  "name": null,
                  "kind": "LIST"
                }
              }
            }
          ]
        },
        {
          "name": "__DirectiveLocation",
          "kind": "ENUM",
          "description": "A Directive can be adjacent to many parts of the GraphQL language, a __DirectiveLocation describes one such possible adjacencies.",
          "fields": null
        }
      ]
    }
  }
}