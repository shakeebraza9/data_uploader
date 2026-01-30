from ExportRecord.DataPrefix import DataPrefix

class DataFomater:
    def __init__(self,data):
        # self.data = self.google_sheet_to_json(GOOGLE_SHEET_LINK)
        self.data = data
    
    
        
            
   
        
    def Render(self,auction_house,LoginToken):
    
        body_id=DataPrefix.SetBodytype(self.data.get("body_id"),auction_house)
     
        return {
        
            'title': self.data.get('title'),
            # 'make_id': DataPrefix.SetMake(self.data.get("make_id")),
            # 'model_id': DataPrefix.SetModel(self.data.get("make_id"),self.data.get("model_id"),self.data.get("variant_id")),
            # 'variant_id': DataPrefix.SetVarient(self.data.get("make_id"),self.data.get("model_id"),self.data.get("variant_id"),auction_house),
            # 'body_id':DataPrefix.Bodydtype(self.data.get("body_id")) ,
            # 'vehicle_id':DataPrefix.VehicleType(DataPrefix.Bodydtype(self.data.get("body_id"))) ,
            'make_id': self.data.get("make_id"),
            'model_id': self.data.get("model_id"),
            'variant_id': "",
            'derivative': self.data.get("variant_id"),
            'body_id':body_id,
            'vehicle_id':None,
            'year': self.data.get('year'),
            'center_id': self.data.get('center_id'),
            'color': self.data.get('color'),
            'vin': self.data.get('vin'),
            'lot': self.data.get('lot'),

            # # Vehicle Specs
            'doors': self.data.get('doors'),
            'seats':self.data.get('seats'),
            # 'fuel_type': DataPrefix.FuleType(self.data.get('fuel_type')),
            'fuel_type': self.data.get('fuel_type'),
            'fuel_details': self.data.get('fuel_type'),
            # 'transmission': DataPrefix.TransmissionType(self.data.get('transmission')),
            'transmission': self.data.get('transmission'),
            'transmission_details': self.data.get('transmission'),
            'cc': self.data.get('cc'),
            'keys': self.data.get('keys'),
            'engine_runs': self.data.get('engine_runs'),
            'mileage': self.data.get("mileage",0),
            'mileage_warranted': self.data.get('mileage_warranted'),
            'former_keepers': self.data.get('former_keepers'),
            'vat_status': self.data.get('vat_status'),

            # # Dates
            'start_date': self.data.get('start_date'),
            'end_date': self.data.get('end_date'),
            'mot_expiry_date': self.data.get('mot_expiry_date'),
            'mot_due': self.data.get('mot_due'),
            'inspection_date': self.data.get('inspection_date'),
            'dor': self.data.get('dor'),
            
            
            # # Documents & Reports
            'v5': self.data.get('v5'),
            'reg': self.data.get('reg') or self.data.get("reg"),
            'service_history': self.data.get('service_history'),
            'no_of_services': self.data.get('no_of_services'),
            'number_of_services_details': self.data.get('number_of_services_details'),
            'last_service': self.data.get('last_service'),
            'last_service_mileage': self.data.get('last_service_mileage'),
            'dvsa_mileage': self.data.get('dvsa_mileage'),
            'inspection_report': self.data.get('inspection_report'),
            'other_report': self.data.get('other_report'),
            'service_notes': self.data.get('service_notes'),
            'vendor': self.data.get('vendor'),
            
            'bidding_history': self.data.get('bidding_history'),
            'last_bid': int(self.data.get('last_bid') or 0),
            'bidding_status': self.data.get('bidding_status'),
            
            # #  Condition & Features
            'grade': self.data.get('grade', ""),
            'tyres_condition': self.data.get('tyres_condition'),
            'general_condition': self.data.get('general_condition'),
            'brakes': self.data.get('brakes'),
            'hubs': self.data.get('hubs'),
            'features': self.data.get('features'),
            'equipment': self.data.get('equipment'),
            'additional_information': self.data.get('additional_information'),
            'imported': self.data.get('imported'),
            'declarations': self.data.get('declarations'),
            'damaged_images': self.data.get('damaged_images'),
            'damage_details': self.data.get('damage_details'),

            # # Media
            'images': self.data.get('images'),
        }

    
