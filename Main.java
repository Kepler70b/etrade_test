import java.io.*;
import java.util.*;
import java.sql.*;
import javax.sql.*;
import javax.xml.parsers.*;
import org.w3c.dom.*;
import oracle.jdbc.OracleDatabaseMetaData;

public class Main {

    static HashMap<String,String> typeMap = new HashMap<String,String>();
    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Usage: java Main <config-file>");
            return;
        }

        String configFilePath = args[0];
        String sqld_file=args[1];
        String work_dir=args[2];
        Properties config = loadConfig(configFilePath);
        if (config == null) {
            System.out.println("Failed to load configuration.");
            return;
        }

        String dbUrl = config.getProperty("db.url");
        String dbUser = config.getProperty("db.user");
        String dbPassword = config.getProperty("db.password");

        try (Connection conn = DriverManager.getConnection(dbUrl, dbUser, dbPassword)) {
            DatabaseMetaData metaData = conn.getMetaData();
            if (metaData instanceof OracleDatabaseMetaData) {
                OracleDatabaseMetaData oracleMetaData = (OracleDatabaseMetaData) metaData;
                String dbVersion = oracleMetaData.getDatabaseProductVersion();
                System.out.println("Connected to Oracle Database version: " + dbVersion);
            } else {
                System.out.println("Connected to non-Oracle database.");
            }
        } catch (SQLException e) {
            e.printStackTrace();
            System.out.println("Database connection failed.");
        }

        try{
            File sqld=new file(sqld_file);
            Document doc= dbuilder.parse(sqld);
            Element root= doc.getDocument();
            NodeList node_list=root.getChildNodes();
            String url=null;
            String user=null;
            String password=null;
            String schema_str=null;
            BufferedWriter m_bw=new BufferedWriter(new FileWriter(metaData_file));
            for(int i=0;i<node_list.getLength();i++){
                Node node=node_list.item(i);
                int type=node.getNodeType();
                if(type==Node.ELEMENT_NODE){
                    processNode(node);
                }
                NamedNodeMap attrs=node.getAtributes();
                for(int j=0;j<attrs.getLength();j++){
                    Node attr=attrs.item(j);
                    String attrName=attr.getNodeName();
                    String attrVal=attr.getNodeValue();

                    if(attrName=='url'){
                        url=attrVal
                    }
                    if(attrName=='user'){
                        user=attrVal
                    }
                    if(attrName=='password'){
                        password=attrVal
                    }
                    if(attrName=='schema'){
                        schema_str=attrVal
                    }
                    handleAttribute(attrName,attrVal);

                    Properties sysProps=System.getProperties();
                    sysProps.put("DYNAMIC_PREPARE","true");
                    sysProps.put("USER",user);
                    sysProps.put("PASSWORD",password);
                    Connection conn=DriverManager.getConnection(url,user,password);
                    String alter_sql="ALTER SESSION SET CURRENT_SCHEMA=";
                    alter_sql=alter_sql+schema_str;
                    Statement stmtSchema=conn.createStatement();
                    int check=stmtSchema.executeUpdate(alter_sql);
                }
            }
        }catch(Exception e){
            e.printStackTrace();
        }
    }
