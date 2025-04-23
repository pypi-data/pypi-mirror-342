from kvprocessor import LoadEnv, KVProcessor

if __name__ == "__main__":
    self.kv_file_path = "test/test.kv"
    self.kv_processor = KVProcessor(self.kv_file_path)
    self.env_list = LoadEnv(self.kv_processor.return_names())
    self.validated_config = self.kv_processor.process_config(self.env_list)
    print(self.validated_config)