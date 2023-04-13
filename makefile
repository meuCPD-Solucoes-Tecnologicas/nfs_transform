PATH_ZIP = log
FILENAME = $(shell date +%Y-%m-%d_%H:%M:%S)log.zip
TARGET_FOLDER= /home/$(USER)/Documentos
generate:
	python ./nfs_complementares.py NFS/Originais NFS/Complementares NFS/Base

generate_and_send:
	python  ./nfs_complementares.py --envio-producao NFS/Originais NFS/Complementares NFS/Base 

generate_and_homo:
	python  ./nfs_complementares.py --envio-homologacao NFS/Originais NFS/Complementares NFS/Base 
	python  ./nfs_complementares.py --envio-homologacao\
	 home/dev/Downloads/enviando_nfes_complementares/novembro/MES\ 11\ SERIE\ 1\
	  NFS/Complementares NFS/Base 

limpeza:
	rm -rf ./NFS/Complementares/*
	rm -rf ./NFS/Dicts_original/*
	rm -rf ./consultas/*

limpeza-logs-and-zip:
	zip -r $(FILENAME) $(PATH_ZIP)
	mv  $(FILENAME) $(TARGET_FOLDER)
	rm -r ./log/*
	
	

limpeza-geral:
	rm -rf ./NFS/Complementares/*
	rm -rf ./NFS/Dicts_original/*
	rm -rf ./consultas/*
	rm -rf ./log/*
	
testa_consultas:
	cp testa_consultadas.py consultas;\
	cd consultas;\
	python testa_consultadas.py;\
	code falharam

teste_sequencia:
	python checa_seq_series.py