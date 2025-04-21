from app.mongo import Conn
from bson.objectid import ObjectId
import json


# TODO: AJ: Revisit the need for this class & the constructor design choice
class ReadWriteOperation(object):
    """

    """

    def __init__(self, user_id_no):
        """

        :param user_id_no:
        """
        user_vendor_info = Conn().vendor_info.find_one({"user_id": user_id_no})
        cust_info = Conn().customer_info.find_one({"_id": ObjectId(user_id_no)}, {"rto_address": 1})

        self.__configured_vendor_accounts = user_vendor_info.get("accounts", {}) if user_vendor_info else {}
        self.__rto_address = cust_info.get('rto_address', {}) if cust_info else {}

    def get_the_active_accounts_list(self, slug):
        """

        :param slug:
        :return:
        """
        list_of_acc_no = []
        configured_vendor_accounts = self.__configured_vendor_accounts
        if configured_vendor_accounts.get(slug):
            for carrier_setting in configured_vendor_accounts.get(slug):
                if configured_vendor_accounts.get(slug).get(carrier_setting, {}).get("is_delete"):
                    continue
                elif configured_vendor_accounts.get(slug).get(carrier_setting, {}).get("is_enabled"):
                    list_of_acc_no.append(carrier_setting)
                else:
                    continue
            return list_of_acc_no
        else:
            return list_of_acc_no

    def get_the_keys(self, vendor_id, slug):
        """

        :param vendor_id:
        :param slug:
        :return:
        """
        return self.__configured_vendor_accounts.get(slug, {}).get(vendor_id)

    def get_active_rto_address(self):
        """

        :return:
        """
        if self.__rto_address:
            for wh_id in self.__rto_address:
                if wh_id:
                    wh_add = self.__rto_address.get(wh_id)
                    if wh_add.get('is_primary', False):
                        return wh_add
        return None

    @staticmethod
    def get_vendor_data(user_id, vendor_id, slug):

        #   user_id -- > api key
        #   list_of_slugs ==> [] list of slugs
        #   list of slugs coz easy post has multiples slugs
        q = "accounts.{slug}.{vendor_id}".format(slug=slug, vendor_id=vendor_id)
        docs = Conn().vendor_info.find_one({"user_id": user_id}, {q: 1})
        return docs.get('accounts', {}).get(slug, {}).get(vendor_id, {})

    @staticmethod
    def get_all_activate_slugs_user(user_id, list_of_slugs, only_slug=False):

        #   user_id -- > api key
        #   list_of_slugs ==> [] list of slugs
        #   list of slugs coz easy post has multiples slugs

        carriers = []
        print("get_all_activate_slugs_perticular_user", user_id, list_of_slugs, only_slug)
        r = {}
        docs = Conn().vendor_info.find_one({"user_id": user_id})
        for slugs in docs.get("accounts"):
            if slugs in list_of_slugs:
                v_id = []
                for vendor_ids in docs["accounts"][slugs]:
                    if docs["accounts"][slugs][vendor_ids]['is_enabled']:
                        v_id.append(vendor_ids)
                carriers.append({
                    slugs: v_id
                })

        return carriers


if __name__ == "__main__":
    s = ['dhl_ecommerce_asia', 'usps']
    d = ReadWriteOperation.get_vendor_data("5d7602492279c10009ef1281", "9463449710", 'usps')
    print(json.dumps(d, indent=4))
